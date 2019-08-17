import socket

http_encoding = 'utf-8'


def start_http_server(port, address='0.0.0.0', extraRoutes={}, metricsRoute='/metrics'):
    bind_address = (address, port)

    http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_socket.bind(bind_address)
    http_socket.listen(1)

    return http_socket


def await_http_request(server_socket, registry):
    conn, addr = server_socket.accept()
    req = conn.recv(1024).decode(http_encoding)

    print('Connection from {}'.format(addr))

    line_break = '\n'.encode(http_encoding)
    content_lines = registry.print()

    content_data = '\n'.join(content_lines).encode(http_encoding)
    content_length = len(content_data)
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
