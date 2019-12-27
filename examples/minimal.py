# library
from prometheus_express import check_network, start_http_server, CollectorRegistry, Counter, Gauge, Router
#from prometheus_express.i2c import scan_i2c_bus

#def check_network(eth):
#  print('check')
#  return True

# system
import board
import busio
import digitalio
import random
import time

# hardware
import neopixel
import wiznet

# colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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

    registry = CollectorRegistry(namespace='prom_express')
    metric_c = Counter('test_counter',
                       'a test counter', registry=registry)
    metric_g = Gauge('test_gauge',
                     'a test gauge', registry=registry)

    router = Router([
        ('GET', '/favicon.ico', lambda headers, body: {
            'status': '200 OK',
            'type': 'image/png;base64',
            'content': 'iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAIAAAD91JpzAAAAFklEQVQI12N8HmPBxMPHxMTDx8TNBwAUNwHSqFS0zAAAAABJRU5ErkJggg==',
        }),
        ('GET', '/metrics', registry.handler),
    ])
    server = False

    rgb[0] = RED  # starting
    while not ready:
        ready = check_network(eth)
        led.value = ready

    rgb[0] = BLUE  # connected
    while not server:
        server = start_http_server(8080, address=eth.ifconfig()[0])

    rgb[0] = GREEN  # ready
    while True:
        metric_c.inc(random.randint(0, 50))
        metric_g.set(random.randint(0, 5000))
        try:
            server.accept(router)
        except OSError as err:
            print('Error accepting request: {}'.format(err))
            server = start_http_server(8080, address=eth.ifconfig()[0])


main()
