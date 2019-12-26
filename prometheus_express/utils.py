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

def scan_i2c_bus(bus, timeout):
    attempt = 0
    while not bus.try_lock():
        if attempt < timeout:
            attempt += 1
        else:
            return False

    print('I2C devices:', [
        hex(x) for x in bus.scan()
    ])
    bus.unlock()
    return True