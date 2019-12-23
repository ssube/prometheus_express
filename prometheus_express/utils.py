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


def scan_i2c_bus(i2c, timeout=10):
    attempt=0

    while not i2c.try_lock():
        if attempt < timeout:
            attempt += 1
            pass
        else:
            return False

    print('I2C devices:', [
        hex(x) for x in i2c.scan()
    ])

    i2c.unlock()
    return True

class CPythonNetwork(object):
    connected = True

    def __init__(self, socket):
        self.socket = socket

    def ifconfig(self):
        hostname = self.socket.gethostname()
        ip_addr = self.socket.gethostbyname(hostname)
        return (ip_addr, 0, 0, 0)