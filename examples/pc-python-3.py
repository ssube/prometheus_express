#! /usr/bin/env python3

# custom
from prometheus_express.metric import Counter, Gauge, Summary
from prometheus_express.registry import CollectorRegistry
from prometheus_express.router import Router
from prometheus_express.server import start_http_server
from prometheus_express.utils import check_network

# system
import random
import socket

class CPythonNetwork():
    connected = True

    def __init__(self, socket):
        self.socket = socket

    def ifconfig(self):
        hostname = self.socket.gethostname()
        ip_addr = self.socket.gethostbyname(hostname)
        return (ip_addr, 0, 0, 0)

# colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

rgb = [()]
eth = CPythonNetwork(socket)

def main():
    ready = False

    registry = CollectorRegistry(namespace='prom_express')
    metric_t = Counter('si7021_temperature',
                       'temperature from the si7021 sensor', ['random_tag'], registry=registry)
    metric_h = Gauge('si7021_humidity',
                     'humidity from the si7021 sensor', ['random_tag'], registry=registry)
    metric_s = Summary('si7021_random', 'random data', [
                       'random_tag'], registry=registry)

    router = Router()
    router.register('GET', '/metrics', registry.handler)
    server = False

    rgb[0] = RED  # starting
    while not ready:
        ready = check_network(eth)

    while True:
        rgb[0] = BLUE  # connected
        while not server:
            server = start_http_server(8080, address=eth.ifconfig()[0])

        rgb[0] = GREEN  # ready
        metric_h.labels(str(random.randint(1, 5))).set(random.randint(25, 100))
        metric_t.labels(str(random.randint(1, 5))).inc(random.randint(1, 5))
        metric_s.labels(str(random.randint(1, 5))).observe(
            random.randint(0, 15))

        try:
            server.accept(router)
        except socket.timeout:
            pass
        except OSError as err:
            print('Error accepting request: {}'.format(err))
        except ValueError as err:
            print('Error parsing request: {}'.format(err))


main()
