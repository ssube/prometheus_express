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

class ValidateNameTest(unittest.TestCase):
  def test(self):
    self.assertEqual(pm.validate_name('foo_bar'), True)
    self.assertEqual(pm.validate_name('123_bar'), False)
    self.assertEqual(pm.validate_name('no!good?'), False)

class MetricNameTest(unittest.TestCase):
  def test_numeric(self):
    with self.assertRaises(ValueError):
      pm.Metric('123_bar', 'invalid name')

  def test_special(self):
    with self.assertRaises(ValueError):
      pm.Metric('no!good?', 'invalid name')

class MetricRenderTest(unittest.TestCase):
  def test(self):
    m = pm.Metric('bin', 'bin values', [
      'key_1', 'key_2',
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
      'key_1', 'key_2',
    ])
    m.labels('value-1', 'value-2')
    m.inc(90)

    r = m.render('foo')
    self.assertEqual([
      '# HELP foo_bin bin values',
      '# TYPE foo_bin counter',
    ], r[:2])

    v = r[2:]
    v.sort()
    self.assertEqual([
      'foo_bin{key_1="None",key_2="None"} 0',
      'foo_bin{key_1="value-1",key_2="value-2"} 90',
    ], v)
