# custom
from prometheus_express.metric import Gauge
from prometheus_express.registry import CollectorRegistry
from prometheus_express.router import Router
from prometheus_express.server import start_http_server
from prometheus_express.utils import check_network, scan_i2c_bus

# system
import board
import busio
import digitalio
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

# set up and scan i2c bus
i2c = busio.I2C(board.SCL, board.SDA)
scan_i2c_bus(i2c, 10)

# set up sensors
sensor_bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
sensor_bme680.sea_level_pressure = 1013.25

sensor_si7021 = adafruit_si7021.SI7021(i2c)

# set up networking
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)

eth = wiznet.WIZNET5K(spi, board.D10, board.D11)
eth.dhcp = True

try:
    eth.config(dhcp_hostname='prometheus_express_m4')
except AttributeError as err:
    print('Error setting hostname:', err)

# initialize the LEDs
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

rgb = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)


def main():
    ready = False

    registry = CollectorRegistry(namespace='prom_express')
    metric_gas = Gauge('gas',
                       'gas from the bme680 sensor', registry=registry)
    metric_humidity = Gauge('humidity',
                            'humidity from both sensors', ['sensor'], registry=registry)
    metric_pressure = Gauge('pressure',
                            'pressure from the bme680 sensor', registry=registry)
    metric_temperature = Gauge('temperature',
                               'temperature from both sensors', ['sensor'], registry=registry)

    router = Router()
    router.register('GET', '/metrics', registry.handler)
    server = False

    rgb[0] = RED  # starting
    while not ready:
        time.sleep(0.5)
        ready = check_network(eth)
        led.value = ready

    while True:
        rgb[0] = BLUE  # connected
        while not server:
            server = start_http_server(8080, address=eth.ifconfig()[0])

        rgb[0] = GREEN  # ready
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
        except ValueError as err:
            print('Error parsing request: {}'.format(err))


main()
