import socket

http_break = '\r\n'
http_encoding = 'utf-8'


def start_http_server(port, address='0.0.0.0', extraRoutes={}, metricsRoute='/metrics'):
    bind_address = (address, port)

    http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_socket.bind(bind_address)
    http_socket.listen(1)

    return http_socket


def await_http_request(server_socket, router):
    conn, addr = server_socket.accept()
    print('Connection: {}'.format(addr))

    req = conn.recv(1024).decode(http_encoding)
    req_headers = parse_headers(req)
    print('Headers: {}'.format(req_headers))

    handler = router.select(req_headers['method'], req_headers['path'])
    resp = handler(req_headers, '')

    if 'type' in resp:
        send_http_response(conn, resp['status'], resp['content'], type=resp['type'])
    else:
        send_http_response(conn, resp['status'], resp['content'])


def send_http_response(conn, status, body, type='text/plain'):
    content_data = body.encode(http_encoding)
    content_length = len(content_data)

    line_break = http_break.encode(http_encoding)
    headers = print_http_headers(status=status, type=type, length=content_length)

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
        raise ValueError('request does not have HTTP/x.y marker')

    lines = req.split(http_break)
    start = lines[0].split(' ')

    return {
        'method': start[0],
        'path': start[1],
        'http': start[2],
    }
