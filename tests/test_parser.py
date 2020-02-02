import prometheus_express.parser as pa
import unittest
from unittest.mock import mock_open, patch


class ParseStrTest(unittest.TestCase):
    def test_simple(self):
        data = pa.parse_str([
            'foo: 1',
            'bar: str',
        ])
        self.assertDictEqual(data, {
            'bar': 'str',
            'foo': '1',
        })

    def test_blanks(self):
        data = pa.parse_str([
            '',
            'foo: 1',
        ])
        self.assertDictEqual(data, {
            'foo': '1',
        })

    def test_comments(self):
        data = pa.parse_str([
            '# ignore: me',
            'foo: 1',
        ])
        self.assertDictEqual(data, {
            'foo': '1',
        })

    def test_invalid(self):
        data = pa.parse_str([
            'foo:',
            'bar: 3',
            'fin',
        ])
        self.assertDictEqual(data, {
            'bar': '3',
        })

class ParseFileTest(unittest.TestCase):
  def test_simple(self):
    mock = unittest.mock.mock_open(read_data='''
    foo: 1
    ''')

    data = pa.parse_file('foo', open=mock)
    self.assertDictEqual(data, {
      'foo': '1',
    })