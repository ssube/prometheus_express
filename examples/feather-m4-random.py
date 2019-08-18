# custom
from prometheus_express.metric import Counter, Gauge
from prometheus_express.registry import CollectorRegistry
from prometheus_express.router import Router
from prometheus_express.server import start_http_server
from prometheus_express.utils import check_network

# system
import board
import busio
import digitalio
import random
import socket
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
led.value = check_network()


def bind():
    ip_addr = eth.ifconfig()[0]
    ip_port = 8080

    print('Binding: {}:{}'.format(ip_addr, ip_port))
    return (start_http_server(ip_port, address=ip_addr), True)


def main():
    ready = False
    bound = False

    registry = CollectorRegistry(namespace='prom_express')
    metric_c = Counter('test_counter',
                       'a test counter', registry=registry)
    metric_g = Gauge('test_gauge',
                     'a test gauge', registry=registry)

    def icon_handler(headers, body):
        return {
            'status': '200 OK',
            'type': 'image/png;base64',
            'content': 'iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAIAAAD91JpzAAAAFklEQVQI12N8HmPBxMPHxMTDx8TNBwAUNwHSqFS0zAAAAABJRU5ErkJggg==',
        }

    def prom_handler(headers, body):
        return {
            'status': '200 OK',
            'content': '\r\n'.join(registry.print()),
        }

    router = Router([
        ('GET', '/favicon.ico', icon_handler),
        ('GET', '/metrics', prom_handler),
    ])
    server = False

    rgb[0] = RED  # starting
    while not ready:
        ready = check_network()

    rgb[0] = BLUE  # connected
    while not bound:
        server, bound = bind()

    rgb[0] = GREEN  # ready
    while True:
        metric_c.inc(random.randint(0, 50))
        metric_g.set(random.randint(0, 5000))
        try:
            server.accept(router)
        except OSError as err:
            print('Error accepting request: {}'.format(err))
            server, bound = bind()


main()
