import prometheus_express.metric as pm
import unittest

class RenderHelpTest(unittest.TestCase):
  def test(self):
    self.assertEqual([
      '# HELP foo bar',
      '# TYPE foo bin',
    ], pm.render_help('foo', 'bar', 'bin'))

class RenderLabelsTest(unittest.TestCase):
  def test_render(self):
    self.assertEqual(
      '{foo="bar",bin="baz"}',
      pm.render_labels([
        'foo', 'bin',
      ], [
        'bar', 'baz',
      ])
    )

  def test_uneven(self):
    with self.assertRaises(ValueError):
      pm.render_labels([
        'key-1', 'key-2',
      ], [
        'value-1',
      ])

  def test_empty(self):
    self.assertEqual('', pm.render_labels([], []))

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

class ValidateMetricTest(unittest.TestCase):
  def test_name_numeric(self):
    with self.assertRaises(ValueError):
      pm.Metric('123_bar', 'invalid name')

  def test_name_special(self):
    with self.assertRaises(ValueError):
      pm.Metric('no!good?', 'invalid name')

  def test_label_numeric(self):
    with self.assertRaises(ValueError):
      pm.Metric('valid', 'also valid', ['123_bar'])

  def test_label_special(self):
    with self.assertRaises(ValueError):
      pm.Metric('valid', 'also valid', ['no!good?'])

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
  def test_simple(self):
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

  '''
  ensure repeated label sets are combined and values
  are accumulated correctly
  '''
  def test_repeat_labels(self):
    m = pm.Counter('bin', 'bin values', [
      'key_1', 'key_2',
    ])
    m.labels('value-1', 'value-2')
    m.inc(30)

    m.labels('foo-1', 'foo-2')
    m.inc(20)

    m.labels('value-1', 'value-2')
    m.inc(60)

    r = m.render('foo')
    v = r[2:]
    v.sort()
    self.assertEqual([
      'foo_bin{key_1="None",key_2="None"} 0',
      'foo_bin{key_1="foo-1",key_2="foo-2"} 20',
      'foo_bin{key_1="value-1",key_2="value-2"} 90',
    ], v)

class CounterValueTest(unittest.TestCase):
  def test_existing(self):
    c = pm.Counter('foo', 'foo values')
    c.inc(20)
    self.assertEqual(c.values[c.emptyLabels], 20)
    c.dec(10)
    self.assertEqual(c.values[c.emptyLabels], 10)

  def test_fresh(self):
    c = pm.Counter('foo', 'foo values', ['bar'])
    c.labels('bin').dec(30)
    self.assertEqual(c.values[('bin',)], -30)

class GaugeValueTest(unittest.TestCase):
  def test_empty(self):
    g = pm.Gauge('foo', 'foo values')
    g.inc(90)
    self.assertEqual(g.values[g.emptyLabels], 90)
    g.set(40)
    self.assertEqual(g.values[g.emptyLabels], 40)

  def test_tuple(self):
    g = pm.Gauge('foo', 'foo values')
    g.set(100)
    self.assertEqual(g.values[()], 100)

class SummaryRenderTest(unittest.TestCase):
  def test(self):
    m = pm.Summary('foo', 'foo values', ['group'])
    m.labels('foo').observe(4)
    m.labels('bar').observe(2)
    m.labels('foo').observe(6)
    m.labels('bar').observe(8)

    r = m.render('bar')
    self.assertEqual(len(r), 8, 'should have 2 lines of help and 6 values')
    self.assertEqual(r[:2], [
      '# HELP bar_foo foo values',
      '# TYPE bar_foo summary',
    ], 'should begin with the help and type lines')

    v = r[2:]
    v.sort()
    self.assertEqual([
      'bar_foo_count{group="None"} 0',
      'bar_foo_count{group="bar"} 2',
      'bar_foo_count{group="foo"} 2',
      'bar_foo_total{group="None"} 0',
      'bar_foo_total{group="bar"} 10',
      'bar_foo_total{group="foo"} 10',
    ], v)