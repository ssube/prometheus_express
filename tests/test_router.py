import unittest
import prometheus_express.router as pr


class ErrorTest(unittest.TestCase):
    def test(self):
        r = pr.errorHandler('', '')
        self.assertEqual(r['status'], '404 Not Found')


class RouterTest(unittest.TestCase):
    def test_missing(self):
        r = pr.Router()
        r.register('GET', '/foo', lambda headers, body: '')

        h = r.select('GET', '/bar')
        self.assertEqual(h, pr.errorHandler)

    def test_match(self):
        def c(headers, body): return ''
        r = pr.Router()
        r.register('GET', '/foo', c)

        h = r.select('GET', '/foo')
        self.assertEqual(h, c)

    def test_register(self):
        r = pr.Router()
        r.register('GET', '/foo', lambda headers, body: '')

        self.assertEqual(len(r), 1)

    def test_contains(self):
        r = pr.Router()
        r.register('GET', '/foo', lambda headers, body: '')

        self.assertTrue(('GET', '/foo') in r)
