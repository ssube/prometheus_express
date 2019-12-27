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

  def test_render(self):
    r = pr.CollectorRegistry()
    pm.Metric('foo', 'foo counts', registry=r)

    lines = r.render()
    self.assertEqual(lines, [
      '# HELP foo foo counts',
      '# TYPE foo untyped',
    ])

  def test_handler(self):
    r = pr.CollectorRegistry()
    pm.Metric('foo', 'foo counts', registry=r)

    self.assertEqual(
      r.handler([], ''),
      {
        'status': '200 OK',
        'content': '# HELP foo foo counts\n# TYPE foo untyped',
      })