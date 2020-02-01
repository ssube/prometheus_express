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
    """List and print devices on the provided I2C bus."""
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

def temp_ftoc(temp_f):
    """Convert fahrenheit degrees to celsius.
    Prometheus expects SI units, but some sensors return F.
    """
    return (temp_f - 32.0) * (5.0 / 9.0)