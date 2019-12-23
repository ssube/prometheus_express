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