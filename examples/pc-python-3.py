#! /usr/bin/env python3

# custom
from prometheus_express.metric import Counter, Gauge
from prometheus_express.registry import CollectorRegistry
from prometheus_express.router import Router
from prometheus_express.server import start_http_server
from prometheus_express.utils import check_network

# system
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

def bind(eth):
    ip_addr = eth.ifconfig()[0]
    ip_port = 8080

    print('Binding: {}:{}'.format(ip_addr, ip_port))
    return (start_http_server(ip_port, address=ip_addr), True)


def main():
    ready = False
    bound = False

    registry = CollectorRegistry(namespace='prom_express')
    metric_t = Gauge('si7021_temperature',
                     'temperature from the si7021 sensor', registry=registry)
    metric_h = Gauge('si7021_humidity',
                     'humidity from the si7021 sensor', registry=registry)

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
        server, bound = bind(eth)

    rgb[0] = GREEN  # ready
    while True:
        metric_h.set(50)
        metric_t.set(25)
        try:
            server.accept(router)
        except OSError as err:
            print('Error accepting request: {}'.format(err))
            server, bound = bind(eth)


main()
