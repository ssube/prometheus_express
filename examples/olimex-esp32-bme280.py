# library
from prometheus_express import check_network, parse_file, start_http_server, temp_ftoc, CollectorRegistry, Counter, Gauge, Router
from bme280 import BME280

# system
import esp32
import machine
import network
import os
import time


def bind(eth, config):
    ip = eth.ifconfig()[0]
    port = int(config['server_port'])
    print('Binding server: {}:{}'.format(ip, port))

    return start_http_server(port, address=ip)


def main():
    # setup sensors
    bus = machine.I2C(scl=machine.Pin(16), sda=machine.Pin(13))
    bme = BME280(i2c=bus)

    # setup storage
    card = machine.SDCard()
    os.mount(card, '/card')

    # setup networking
    config = load_config('/card', 'config.yml')
    eth = start_network(config)

    # setup Prometheus metrics
    registry = CollectorRegistry(namespace='prometheus_express')
    metric_c = Counter(
        'system_heartbeat',
        'system heartbeat counter',
        labels=['location'],
        registry=registry
    )
    metric_g = Gauge(
        'sensor_temperature',
        'temperature data from the sensors',
        labels=['location', 'sensor'],
        registry=registry
    )

    router = Router()
    router.register('GET', '/metrics', registry.handler)
    server = False

    # wait for incoming connection
    while True:
        while not server:
            time.sleep(1)
            server = bind(eth, config)

        location = config['metric_location']
        metric_c.labels(location).inc(1)
        metric_g.labels(location, 'esp32').set(temp_ftoc(esp32.raw_temperature()))
        metric_g.labels(location, 'bme280').set(bme.read_compensated_data()[0])

        try:
            server.accept(router)
        except OSError as err:
            print('Error accepting request: {}'.format(err))
        except ValueError as err:
            print('Error parsing request: {}'.format(err))


main()
