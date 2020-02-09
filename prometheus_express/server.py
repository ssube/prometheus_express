import socket

http_break = '\r\n'
http_encoding = 'utf-8'
http_default_status = '200 OK'
http_default_type = 'text/plain'


def start_http_server(port, address='0.0.0.0', depth=2, timeout=5.0):
    bind_address = (address, port)

    http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # lgtm [py/bind-socket-all-network-interfaces]
    http_socket.bind(bind_address)
    http_socket.listen(depth)

    try:
        http_socket.settimeout(timeout)
    except OSError as err:
        print('Unable to set socket timeout:', err)

    return Server(http_socket)


class Server():
    http_socket = False

    def __init__(self, http_socket):
        self.http_socket = http_socket

    def accept(self, router):
        conn, addr = self.http_socket.accept()

        req = conn.recv(1024).decode(http_encoding)
        req_headers, req_body = self.parse_headers(req)

        handler = router.select(req_headers['method'], req_headers['path'])
        resp = handler(req_headers, req_body)

        if 'type' not in resp:
            resp['type'] = http_default_type

        return self.send_response(
            conn,
            resp['status'],
            resp['content'],
            type=resp['type'])

    def send_response(self, conn, status, body, type):
        content_data = body.encode(http_encoding)
        content_length = len(content_data)

        line_break = http_break.encode(http_encoding)
        headers = self.format_headers(
            status=status, type=type, length=content_length)

        try:
            for line in headers:
                conn.send(line.encode(http_encoding))
                conn.send(line_break)

            conn.send(line_break)
            conn.send(content_data)

            conn.close()
        except OSError as err:
            print('Error sending response: {}'.format(err))

    def format_headers(self, status, type, length=0):
        return [
            'HTTP/1.1 {}'.format(status),
            'Connection: close',
            'Content-Type: {}'.format(type),
            'Content-Length: {}'.format(length),
        ]

    def parse_headers(self, req):
        if 'HTTP/' not in req:
            raise ValueError('request does not have HTTP/x.y marker')

        lines = req.split(http_break)
        start = lines[0].split(' ')

        if len(start) < 3:
            raise ValueError('request does not have all HTTP components')

        return ({
            'method': start[0],
            'path': start[1],
            'http': start[2],
        }, '')
