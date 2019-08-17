import socket

http_break = '\r\n'
http_encoding = 'utf-8'


def start_http_server(port, address='0.0.0.0', extraRoutes={}, metricsRoute='/metrics'):
    bind_address = (address, port)

    http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_socket.bind(bind_address)
    http_socket.listen(1)

    try:
        http_socket.settimeout(1.0)
        http_socket.setblocking(0)
    except OSError:
        print('Unable to set timeout on socket')

    return http_socket


def await_http_request(server_socket, registry):
    conn, addr = server_socket.accept()
    print('Connection: {}'.format(addr))

    req = read_http_request(conn)
    req_headers = parse_headers(req)
    print('Headers: {}'.format(req_headers))

    if req_headers['method'] == 'GET' and req_headers['path'] == registry.path:
        metrics = registry.print()
        send_http_response(conn, http_break.join(metrics))
    else:
        send_http_response(conn, 'Hello World!')


def send_http_response(conn, body):
    content_data = body.encode(http_encoding)
    content_length = len(content_data)

    line_break = http_break.encode(http_encoding)
    headers = print_http_headers(length=content_length)

    try:
        for line in headers:
            conn.send(line.encode(http_encoding))
            conn.send(line_break)

        conn.send(line_break)
        conn.send(content_data)

        conn.close()
    except OSError as err:
        print('Error sending response: {}'.format(err))


def print_http_headers(status='200 OK', type='text/plain', length=0):
    return [
        'HTTP/1.1 {}'.format(status),
        'Connection: close',
        'Content-Type: {}'.format(type),
        'Content-Length: {}'.format(length),
    ]


def parse_headers(req):
    if 'HTTP/' not in req:
        print('Body ({}): {}'.format(len(req), req))
        raise ValueError('request does not have HTTP/x.y marker')

    lines = req.split(http_break)
    start = lines[0].split(' ')

    return {
        'method': start[0],
        'path': start[1],
        'http': start[2],
    }


def read_http_request(conn):
    body = bytearray()
    chunk_max = 256

    while True:
        print('body: {}'.format(body))
        chunk = bytearray(b" " * chunk_max)

        bytes = conn.recv_into(chunk, chunk_max)
        print('chunk read: {}'.format(bytes))
        if bytes == 0:
            print('inner body')
            return body.encode(http_encoding)
        else:
            body.extend(chunk)
