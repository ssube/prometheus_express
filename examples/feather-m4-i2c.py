# custom
from prometheus_express.metric import Counter, Gauge
from prometheus_express.registry import CollectorRegistry
from prometheus_express.router import Router
from prometheus_express.server import start_http_server
from prometheus_express.utils import bind_server, check_network

# system
import board
import busio
import digitalio
import socket
import time

# hardware
import adafruit_bme680
import adafruit_si7021
import neopixel
import wiznet

# colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# scan i2c bus
i2c = busio.I2C(board.SCL, board.SDA)
while not i2c.try_lock():
    pass

print([hex(x) for x in i2c.scan()])
i2c.unlock()

# set up sensors
sensor_bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
sensor_bme680.sea_level_pressure = 1013.25

sensor_si7021 = adafruit_si7021.SI7021(i2c)

# set up networking
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)

eth = wiznet.WIZNET5K(spi, board.D10, board.D11)
eth.dhcp = True

# initialize the LEDs
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

rgb = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)

time.sleep(0.5)
led.value = check_network(eth)


def main():
    ready = False
    bound = False

    registry = CollectorRegistry(namespace='prom_express')
    metric_gas = Gauge('gas',
                       'gas from the bme680 sensor', registry=registry)
    metric_humidity = Gauge('humidity',
                            'humidity from both sensors', ['sensor'], registry=registry)
    metric_pressure = Gauge('pressure',
                            'pressure from the bme680 sensor', registry=registry)
    metric_temperature = Gauge('temperature',
                               'temperature from both sensors', ['sensor'], registry=registry)

    def prom_handler(headers, body):
        return {
            'status': '200 OK',
            'content': '\r\n'.join(registry.print()),
        }

    router = Router([
        ('GET', '/metrics', prom_handler),
    ])
    server = False

    rgb[0] = RED  # starting
    while not ready:
        time.sleep(0.5)
        ready = check_network(eth)
        led.value = ready

    rgb[0] = BLUE  # connected
    while not bound:
        server, bound = bind_server(eth)

    rgb[0] = GREEN  # ready
    while True:
        metric_gas.set(sensor_bme680.gas)
        metric_humidity.labels('bme680').set(sensor_bme680.humidity)
        metric_humidity.labels('si7021').set(sensor_si7021.relative_humidity)
        metric_pressure.set(sensor_bme680.pressure)
        metric_temperature.labels('bme680').set(sensor_bme680.temperature)
        metric_temperature.labels('si7021').set(sensor_si7021.temperature)

        try:
            server.accept(router)
        except OSError as err:
            print('Error accepting request: {}'.format(err))
            server, bound = bind_server(eth)
        except Exception as err:
            print('Unknown error: {}'.format(err))


main()
