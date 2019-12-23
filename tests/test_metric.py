import prometheus_express.metric as pm
import unittest

class RenderHelpTest(unittest.TestCase):
  def test(self):
    self.assertEqual([
      '# HELP foo bar',
      '# TYPE foo bin',
    ], pm.render_help('foo', 'bar', 'bin'))

class RenderLabelsTest(unittest.TestCase):
  def test(self):
    self.assertEqual(
      '{foo="bar",bin="baz"}',
      pm.render_labels([
        'foo', 'bin',
      ], [
        'bar', 'baz',
      ])
    )

class RenderNameTest(unittest.TestCase):
  def test(self):
    self.assertEqual(
      'foo_bar',
      pm.render_name('foo', 'bar')
    )

class MetricRenderTest(unittest.TestCase):
  def test(self):
    m = pm.Metric('bin', 'bin values', [
      'key-1', 'key-2',
    ])
    m.labels('value-1', 'value-2')

    r = m.render('foo')
    self.assertEqual([
      '# HELP foo_bin bin values',
      '# TYPE foo_bin untyped',
      # no label/value line
    ], r)

class CounterRenderTest(unittest.TestCase):
  def test(self):
    m = pm.Counter('bin', 'bin values', [
      'key-1', 'key-2',
    ])
    m.labels('value-1', 'value-2')
    m.inc(90)

    r = m.render('foo')
    self.assertEqual([
      '# HELP foo_bin bin values',
      '# TYPE foo_bin counter',
      'foo_bin{key-1="value-1",key-2="value-2"} 90',
      'foo_bin{key-1="None",key-2="None"} 0',
    ], r)
