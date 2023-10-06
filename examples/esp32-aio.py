"""
Very simplistic demo of the asyncio version of prometheus_express
"""
import asyncio
import network
import random
import time

# custom
from prometheus_express.metric import Counter, Gauge, Summary
from prometheus_express.registry import CollectorRegistry
from prometheus_express.router import Router
from prometheus_express.uaioserver import AIOServer

def wifi_up_please():
    """hard syncro just to get wifi, you replace this with your own world view"""
    sta = network.WLAN(network.STA_IF)
    sta.active(False)  # reset interface
    sta.active(True)
    ssid = "hohoho"
    password = "blahblah"
    sta.connect(ssid, password)

    while not sta.isconnected():
        print("waiting for connection")
        time.sleep(1)

    print(f"Connect to: http://{sta.ifconfig()[0]}:8080/metrics")


async def main_aio():

    registry = CollectorRegistry(namespace='prom_express')
    metric_t = Counter('si7021_temperature',
                       'temperature from the si7021 sensor', ['random_tag'], registry=registry)
    metric_h = Gauge('si7021_humidity',
                     'humidity from the si7021 sensor', ['random_tag'], registry=registry)
    metric_s = Summary('si7021_random', 'random data', [
        'random_tag'], registry=registry)

    router = Router()
    router.register('GET', '/metrics', registry.handler)

    s = AIOServer(router)

    asyncio.create_task(s.start_server(8080))

    while True:
        await asyncio.sleep_ms(500)
        metric_h.labels(str(random.randint(1, 5))).set(random.randint(25, 100))
        metric_t.labels(str(random.randint(1, 5))).inc(random.randint(1, 5))
        metric_s.labels(str(random.randint(1, 5))).observe(random.randint(0, 15))


def main():
    wifi_up_please()
    asyncio.run(main_aio())

main()
