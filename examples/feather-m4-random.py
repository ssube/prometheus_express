# library
from prometheus_express import check_network, start_http_server, CollectorRegistry, Counter, Gauge, Router

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
server_port = 8080

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
                       'a test counter',
                       labels=['source'],
                       registry=registry)
    metric_g = Gauge('test_gauge',
                     'a test gauge',
                     labels=['source'],
                     registry=registry)

    router = Router()
    router.register('GET', '/metrics', registry.handler)
    server = False

    rgb[0] = RED  # starting
    while not ready:
        ready = check_network(eth)
        led.value = ready

    while True:
        rgb[0] = BLUE  # connected
        while not server:
            ip = eth.ifconfig()[0]
            print('Binding server: {}'.format(ip))
            server = start_http_server(server_port, address=ip, depth=8)

        rgb[0] = GREEN  # ready
        metric_c.labels('heartbeat').inc(1)
        metric_c.labels('random').inc(random.randint(0, 50))
        metric_g.labels('clock').set(time.time())
        metric_g.labels('random').set(random.randint(0, 5000))

        try:
            server.accept(router)
        except OSError as err:
            print('Error accepting request: {}'.format(err))
        except ValueError as err:
            print('Error parsing request: {}'.format(err))


main()
