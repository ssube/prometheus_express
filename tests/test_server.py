import unittest
import prometheus_express.router as pr
import prometheus_express.server as ps

class MockConnection(object):
  def __init__(self, body):
    self.accum = []
    self.body = body
    self.buffer = []
    self.index = 0
    self.open = True

  def recv(self, n):
    print('recv', n)
    self.buffer = self.body[self.index : self.index + n]
    self.index += n
    return self.buffer.encode(ps.http_encoding)

  def send(self, chunk):
    self.accum.append(chunk)

  def close(self):
    self.open = False

  def response(self):
    return ''.join([x.decode(ps.http_encoding) for x in self.accum])

class MockSocket(object):
  def __init__(self, addr, body):
    self.addr = addr
    self.body = body
    self.conn = MockConnection(self.body)

  def accept(self):
    return (self.conn, self.addr)

class ServerAcceptTest(unittest.TestCase):
  def test_valid(self):
    body = 'test body'
    mock = MockSocket('0.0.0.1', 'GET / HTTP/1.1\r\n{}'.format(body))

    s = ps.Server(mock)
    r = pr.Router()
    r.register('GET', '/', lambda headers, req: {
      'content': body,
      'status': 200,
    })
    s.accept(r)

    result = mock.conn.response()
    self.assertEqual(
      result.split('\r\n')[-1],
      body
    )

  def test_missing_verb(self):
    body = 'test body'
    mock = MockSocket('0.0.0.1', 'HTTP/1.1\r\n{}'.format(body))

    s = ps.Server(mock)
    r = pr.Router()
    r.register('GET', '/', lambda headers, req: body)

    with self.assertRaises(ValueError):
      s.accept(r)
