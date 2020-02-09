# library
from redesigned_barnacle.config import load_config, parse_file
from redesigned_barnacle.eth import eth_start
from redesigned_barnacle.sparkline import Sparkline
from redesigned_barnacle.unit import temp_ftoc
from prometheus_express import start_http_server, CollectorRegistry, Counter, Gauge, Router
from bme280 import BME280
from ssd1306 import SSD1306_I2C

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
    oled = SSD1306_I2C(128, 32, bus)

    # setup storage
    card = machine.SDCard()
    os.mount(card, '/card')

    # setup networking
    config = load_config('/card', 'config.yml')
    eth = eth_start(
        config,
        mdc=machine.Pin(23),
        mdio=machine.Pin(18),
        phy_type=network.PHY_LAN8720,
        phy_addr=0,
        clock_mode=network.ETH_CLOCK_GPIO17_OUT,
        power_pin=machine.Pin(12, machine.Pin.OUT)
    )

    # setup display
    sl = Sparkline(32, 128)
    oled.init_display()
    oled.fill(0x0)
    oled.text('loading', 0, 0)
    oled.show()

    # setup Prometheus metrics
    registry = CollectorRegistry(namespace='prometheus_express')
    metric_beat = Counter(
        'system_heartbeat',
        'system heartbeat counter',
        labels=['location'],
        registry=registry
    )
    metric_temp = Gauge(
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

        bme_reading = bme.read_compensated_data()
        temp_line = ((bme_reading[0] - 12) * 2) % 32
        print('temp line: {}'.format(temp_line))

        oled.fill(0x0)
        sl.push(temp_line)
        sl.draw(oled, 0, 12)
        oled.text(str(bme_reading[0]), 0, 0)
        oled.show()

        location = config['metric_location']
        metric_beat.labels(location).inc(1)
        metric_temp.labels(location, 'esp32').set(
            temp_ftoc(esp32.raw_temperature()))
        metric_temp.labels(location, 'bme280').set(bme_reading[0])

        try:
            server.accept(router)
        except OSError as err:
            print('Error accepting request: {}'.format(err))
        except ValueError as err:
            print('Error parsing request: {}'.format(err))


main()
