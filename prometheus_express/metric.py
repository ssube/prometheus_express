def print_help(name, desc, type):
    return [
        '# HELP {} {}'.format(name, desc),
        '# TYPE {} {}'.format(name, type),
    ]


def print_name(namespace, name):
    if namespace != '':
        return '{}_{}'.format(namespace, name)
    else:
        return name

# base class for metric types


class Metric():
    name = ''
    desc = ''
    labelKeys = []
    metricType = 'untyped'

    def __init__(self, name, desc, labels=[], registry=False):
        self.name = name
        self.desc = desc
        self.labelKeys = labels

        if registry != False:
            registry.register(self)

    # TODO: fluent API for labeling metrics
    def labels(self, *labelValues):
        if len(labelValues) != len(self.labelKeys):
            raise ValueError('length of label values must equal label keys')

        return self

    def print(self, namespace):
        return print_help(print_name(namespace, self.name), self.desc, self.metricType)


class Counter(Metric):
    metricType = 'counter'
    value = 0

    def inc(self, value):
        self.value += value

    def dec(self, value):
        self.value -= value

    def print(self, namespace):
        return super().print(namespace) + [
            '{} {}'.format(print_name(namespace, self.name), self.value)
        ]


class Gauge(Counter):
    metricType = 'gauge'

    def set(self, value):
        self.value = value


class Summary(Metric):
    metricType = 'summary'
    valueCount = 0
    valueTotal = 0

    def observe(self, value):
        self.valueCount += 1
        self.valueTotal += value

    def print(self, namespace):
        nn = print_name(namespace, self.name)
        return print_help(nn + '_count', self.desc, self.metricType) + [
            '{}_count {}'.format(nn, self.valueCount),
        ] + print_help(nn + '_total', self.desc, self.metricType) + [
            '{}_total {}'.format(nn, self.valueTotal),
        ]
