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
        name = self.printName(namespace)
        return [
            '# HELP {} {}'.format(name, self.desc),
            '# TYPE {} {}'.format(name, self.metricType),
        ]

    def printName(self, namespace):
        if namespace != '':
            return '{}_{}'.format(namespace, self.name)
        else:
            return self.name


class Counter(Metric):
    metricType = 'counter'
    value = 0

    def inc(self, value):
        self.value += value

    def dec(self, value):
        self.value -= value

    def print(self, namespace):
        return super().print(namespace) + [
            '{} {}'.format(self.printName(namespace), self.value)
        ]


class Gauge(Counter):
    metricType = 'gauge'

    def set(self, value):
        self.value = value
