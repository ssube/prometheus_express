# library
from prometheus_express import check_network, start_http_server, CollectorRegistry, Counter, Gauge, Router
from si7021 import Si7021
#from bme680 import BME680
#from usmbus import SMBus

# system
import machine
import network
import time

server_port = 8080

#bus = SMBus(scl=machine.Pin(16), sda=machine.Pin(13))
#bme = BME680(i2c_device=bus, i2c_addr=119)
bus = machine.I2C(scl=machine.Pin(16), sda=machine.Pin(13))
sil = Si7021(bus)

def main():
  registry = CollectorRegistry(namespace='prom_esp32')
  metric_c = Counter(
    'test_counter',
    'a test counter',
    labels=['source'],
    registry=registry
  )
  metric_g = Gauge(
    'bme680_temperature',
    'temperature data from the bme680 sensor',
    labels=['source'],
    registry=registry
  )

  router = Router()
  router.register('GET', '/metrics', registry.handler)
  server = False

  # connect to wired LAN
  eth_power = machine.Pin(12, machine.Pin.OUT)
  eth_power.value(1)

  eth = network.LAN(
    mdc = machine.Pin(23),
    mdio = machine.Pin(18),
    phy_type = network.PHY_LAN8720,
    phy_addr = 0,
    clock_mode = network.ETH_CLOCK_GPIO17_OUT
  )
  eth.active(True)

  time.sleep(1)
  net = eth.ifconfig()
  print(net)

  while True:
    while not server:
      time.sleep(1)
      ip = eth.ifconfig()[0]
      print('Binding server: {}'.format(ip))
      server = start_http_server(server_port, address=ip)

    #if bme.get_sensor_data():
    #  metric_c.inc(1)
    #  metric_g.set(bme.data.temperature)
    metric_c.labels('si7021').inc(1)
    metric_g.labels('si7021').set(sil.temperature)

    try:
      server.accept(router)
    except OSError as err:
      print('Error accepting request: {}'.format(err))
    except ValueError as err:
      print('Error parsing request: {}'.format(err))


main()
