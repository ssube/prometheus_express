#! /usr/bin/env python3

# custom
from prometheus_express.metric import Counter, Gauge, Summary
from prometheus_express.registry import CollectorRegistry
from prometheus_express.router import Router
from prometheus_express.server import start_http_server
from prometheus_express.utils import bind_server, check_network

# system
import random
import socket
import time

# colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

rgb = [()]


class Network():
    connected = True

    def ifconfig(self):
        hostname = socket.gethostname()
        ip_addr = socket.gethostbyname(hostname)
        return (ip_addr, 0, 0, 0)


eth = Network()


def main():
    ready = False
    bound = False

    registry = CollectorRegistry(namespace='prom_express')
    metric_t = Counter('si7021_temperature',
                       'temperature from the si7021 sensor', ['random_tag'], registry=registry)
    metric_h = Gauge('si7021_humidity',
                     'humidity from the si7021 sensor', ['random_tag'], registry=registry)
    metric_s = Summary('si7021_random', 'random data', [
                       'random_tag'], registry=registry)

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
        ready = check_network(eth)

    rgb[0] = BLUE  # connected
    while not bound:
        server, bound = bind_server(eth)

    rgb[0] = GREEN  # ready
    while True:
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
            server, bound = bind_server(eth)


main()
