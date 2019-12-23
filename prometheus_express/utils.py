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


def scan_i2c_bus(i2c):
    while not i2c.try_lock():
        pass

    print('I2C devices:', [
        hex(x) for x in i2c.scan()
    ])

    i2c.unlock()
