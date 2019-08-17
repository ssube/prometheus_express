#! /usr/bin/env python3

# custom
from prometheus_express.http import start_http_server, await_http_request
from prometheus_express.metric import Counter, Gauge
from prometheus_express.registry import CollectorRegistry

# system
import socket
import time

# colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

rgb = [()]

def ifconfig():
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    return (ip_addr, 0, 0, 0)

def check_network():
    network = ifconfig()
    online = True

    print('Online: {}'.format(online))
    if online == False:
        return False

    print('Network: {}'.format(network))
    if network[0] == '0.0.0.0':
        return False

    return True


def bind():
    ip_addr = ifconfig()[0]
    ip_port = 8080

    print('Binding: {}:{}'.format(ip_addr, ip_port))
    return (start_http_server(ip_port, address=ip_addr), True)


def main():
    ready = False
    bound = False

    server = False

    registry = CollectorRegistry(namespace='prom_express')
    metric_t = Gauge('si7021_temperature',
                     'temperature from the si7021 sensor', registry=registry)
    metric_h = Gauge('si7021_humidity',
                     'humidity from the si7021 sensor', registry=registry)

    rgb[0] = RED  # starting
    while ready == False:
        ready = check_network()

    rgb[0] = BLUE  # connected
    while bound == False:
        server, bound = bind()

    rgb[0] = GREEN  # ready
    while True:
        metric_h.set(50)
        metric_t.set(25)
        try:
            await_http_request(server, registry)
        except OSError as err:
            print('Error accepting request: {}'.format(err))
            server, bound = bind()


main()
