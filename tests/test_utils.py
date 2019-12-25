import prometheus_express.utils as pu
import unittest

class MockI2C(object):
  def __init__(self, locked=False, devices=[]):
    self.devices = devices
    self.locked = locked

  def try_lock(self):
    if self.locked:
      return False
    else:
      self.locked = True
      return True

  def scan(self):
    return self.devices

  def unlock(self):
    self.locked = False

class MockNetwork(object):
  def __init__(self, connected=False, ip='0.0.0.0'):
    self.connected = connected
    self.ip = ip

  def ifconfig(self):
    return [self.ip]

class CheckNetworkTest(unittest.TestCase):
  def test_unconnected(self):
    self.assertEqual(
      pu.check_network(MockNetwork()),
      False,
    )

  def test_connected_nullip(self):
    self.assertEqual(
      pu.check_network(MockNetwork(connected=True)),
      False,
    )

  def test_connected_withip(self):
    self.assertEqual(
      pu.check_network(MockNetwork(connected=True, ip='1.1.1.1')),
      True,
    )

class ScanI2CBusTest(unittest.TestCase):
  def test_unlocked(self):
    self.assertEqual(
      pu.scan_i2c_bus(MockI2C(), 10),
      True,
    )

  def test_locked(self):
    self.assertEqual(
      pu.scan_i2c_bus(MockI2C(locked=True), 10),
      False,
    )