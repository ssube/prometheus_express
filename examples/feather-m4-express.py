# custom
from prometheus_express.http import start_http_server, await_http_request
from prometheus_express.metric import Counter, Gauge
from prometheus_express.registry import CollectorRegistry

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

    server = False

    registry = CollectorRegistry()
    metric_c = Counter('prom_express_test_counter',
                       'a test counter', registry=registry)
    metric_g = Gauge('prom_express_test_gauge',
                     'a test gauge', registry=registry)

    rgb[0] = RED  # starting
    while ready == False:
        ready = check_network()

    rgb[0] = BLUE  # connected
    while bound == False:
        server, bound = bind()

    rgb[0] = GREEN  # ready
    while True:
        metric_c.inc(random.randint(0, 50))
        metric_g.set(random.randint(0, 5000))
        print('Accepting...')
        try:
            await_http_request(server, registry)
        except OSError as err:
            print('Error accepting request: {}'.format(err))
            server, bound = bind()


main()
