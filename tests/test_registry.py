import prometheus_express.metric as pm
import prometheus_express.registry as pr
import unittest

class RegistryTest(unittest.TestCase):
  def test_register(self):
    m = pm.Metric('foo', 'foo counts')
    r = pr.CollectorRegistry()
    r.register(m)
    r.register(m)
    self.assertEqual(r.metrics, set([m]))