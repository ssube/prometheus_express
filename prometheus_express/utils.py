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