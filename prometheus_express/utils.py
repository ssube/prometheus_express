from prometheus_express.server import start_http_server


def check_network(eth):
    online = eth.connected
    network = eth.ifconfig()

    print('Online: {}'.format(online))
    if not online:
        return False

    print('Network: {}'.format(network))
    if network[0] == '0.0.0.0':
        return False

    return True


def bind_server(eth):
    ip_addr = eth.ifconfig()[0]
    ip_port = 8080

    print('Binding: {}:{}'.format(ip_addr, ip_port))
    return (start_http_server(ip_port, address=ip_addr), True)


def scan_i2c_bus(i2c):
    while not i2c.try_lock():
        pass

    print('I2C devices:', [
        hex(x) for x in i2c.scan()
    ])

    i2c.unlock()
