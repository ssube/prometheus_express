from unittest.mock import MagicMock
import unittest
import prometheus_express.router as pr


class ErrorTest(unittest.TestCase):
    def test(self):
        r = pr.error_handler('', '')
        self.assertEqual(r['status'], '404 Not Found')


class RouterTest(unittest.TestCase):
    def test_missing(self):
        r = pr.Router()
        r.register('GET', '/foo', lambda headers, body: pr.response(''))

        h = r.select('GET', '/bar')
        self.assertEqual(h, pr.error_handler)

    def test_match(self):
        def c(headers, body): return ''
        r = pr.Router()
        r.register('GET', '/foo', c)

        h = r.select('GET', '/foo')
        self.assertEqual(h, c)

    def test_register(self):
        r = pr.Router()
        r.register('GET', '/foo', lambda headers, body: pr.response(''))

        self.assertEqual(len(r), 1)

    def test_contains(self):
        r = pr.Router()
        r.register('GET', '/foo', lambda headers, body: pr.response(''))

        self.assertTrue(('GET', '/foo') in r)

    def test_register_all(self):
        r = pr.Router()
        r.register_all([
            ('GET', '/foo', lambda headers, body: pr.response('')),
            ('POST', '/bar', lambda headers, body: pr.response('')),
        ])

        self.assertEqual(len(r), 2)

    def test_iter(self):
        r = pr.Router()
        r.register_all([
            ('GET', '/foo', lambda headers, body: pr.response('')),
            ('POST', '/bar', lambda headers, body: pr.response('')),
        ])

        methods = [x[0] for x in r]
        self.assertEqual(methods, ['GET', 'POST'])

    def test_register_numeric(self):
        r = pr.Router()

        with self.assertRaises(ValueError):
            r.register('GET', 123, lambda headers, body: pr.response(''))

    def test_register_invalid(self):
        r = pr.Router()

        with self.assertRaises(ValueError):
            r.register('GET', '/', '')


class MiddlewareTest(unittest.TestCase):
    def test_bind(self):
        middleware = [
            MagicMock(return_value=None),
            MagicMock(return_value=None),
        ]
        handler = MagicMock(return_value=pr.response('foo'))

        bound = pr.bind_middleware(handler, middleware)
        headers = {}
        response = bound(headers, '')

        middleware[0].assert_called_once()
        middleware[1].assert_called_once()
        handler.assert_called_once()
        self.assertEqual(response['content'], 'foo')
