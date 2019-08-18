# custom
from prometheus_express.metric import Counter, Gauge
from prometheus_express.registry import CollectorRegistry
from prometheus_express.router import Router
from prometheus_express.server import start_http_server

# system
import board
import busio
import digitalio
import random
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


def check_network():
    online = eth.connected
    network = eth.ifconfig()

    led.value = online

    print('Online: {}'.format(online))
    if online == False:
        return False

    print('Network: {}'.format(network))
    if network[0] == '0.0.0.0':
        return False

    return True


def bind():
    ip_addr = eth.ifconfig()[0]
    ip_port = 8080

    print('Binding: {}:{}'.format(ip_addr, ip_port))
    return (start_http_server(ip_port, address=ip_addr), True)


def main():
    ready = False
    bound = False

    registry = CollectorRegistry(namespace='prom_express')
    metric_gas = Gauge('bme680_gas',
                       'gas from the bme680 sensor', registry=registry)
    metric_humidity = Gauge('bme680_humidity',
                            'humidity from the bme680 sensor', registry=registry)
    metric_humidity2 = Gauge('si7021_humidity',
                             'relative humidity from the si7021 sensor', registry=registry)
    metric_pressure = Gauge('bme680_pressure',
                            'pressure from the bme680 sensor', registry=registry)
    metric_temperature = Gauge('bme680_temperature',
                               'temperature from the bme680 sensor', registry=registry)
    metric_temperature2 = Gauge('si7021_temperature',
                                'temperature from the si7021 sensor', registry=registry)

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
    while ready == False:
        ready = check_network()

    rgb[0] = BLUE  # connected
    while bound == False:
        server, bound = bind()

    rgb[0] = GREEN  # ready
    while True:
        metric_gas.set(sensor_bme680.gas)
        metric_humidity.set(sensor_bme680.humidity)
        metric_humidity2.set(sensor_si7021.relative_humidity)
        metric_pressure.set(sensor_bme680.pressure)
        metric_temperature.set(sensor_bme680.temperature)
        metric_temperature2.set(sensor_si7021.temperature)

        try:
            server.accept(router)
        except OSError as err:
            print('Error accepting request: {}'.format(err))
            server, bound = bind()


main()
