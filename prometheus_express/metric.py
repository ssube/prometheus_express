def print_help(name, desc, type):
    return [
        '# HELP {} {}'.format(name, desc),
        '# TYPE {} {}'.format(name, type),
    ]


def print_labels(keys, values):
    if len(keys) != len(values):
        raise ValueError('length of label values must equal label keys')

    if len(keys) == 0:
        return ''

    labels = []
    for k, v in zip(keys, values):
        labels.append('{}="{}"'.format(k, v))

    return '{' + ','.join(labels) + '}'


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

        self.emptyLabels = (None,) * len(labels)
        self.labelValues = self.emptyLabels
        self.values = {
            self.emptyLabels: 0,
        }

        if registry != False:
            registry.register(self)

    # TODO: fluent API for labeling metrics
    def labels(self, *labelValues):
        #labels = populate_labels(self.labelKeys, labelValues)
        self.labelValues = labelValues
        return self

    def print(self, namespace):
        return print_help(print_name(namespace, self.name), self.desc, self.metricType)


class Counter(Metric):
    metricType = 'counter'

    def inc(self, value):
        if self.labelValues in self.values:
            self.values[self.labelValues] += value
        else:
            self.values[self.labelValues] = value

        self.labelValues = self.emptyLabels

    def dec(self, value):
        if self.labelValues in self.values:
            self.values[self.labelValues] -= value
        else:
            self.values[self.labelValues] = value

        self.labelValues = self.emptyLabels

    def print(self, namespace):
        lines = super().print(namespace)
        for l, v in self.values.items():
            lines.append('{}{} {}'.format(print_name(
                namespace, self.name), print_labels(self.labelKeys, l), v))

        return lines


class Gauge(Counter):
    metricType = 'gauge'

    def set(self, value):
        self.values[self.labelValues] = value
        self.labelValues = self.emptyLabels


class Summary(Metric):
    metricType = 'summary'

    def __init__(self, name, desc, labels=[], registry=False):
        Metric.__init__(self, name, desc, labels, registry=registry)
        self.values = {
            self.emptyLabels: (0, 0),
        }

    def observe(self, value):
        if self.labelValues in self.values:
            prev = self.values.get(self.labelValues)
            self.values[self.labelValues] = (prev[0] + 1, prev[1] + value)
        else:
            self.values[self.labelValues] = (1, value)

    def print(self, namespace):
        nn = print_name(namespace, self.name)
        lines = super().print(namespace)
        for l, v in self.values.items():
            ll = print_labels(self.labelKeys, l)
            lines.extend(print_help(nn + '_count', self.desc, self.metricType))
            lines.append('{}_count{} {}'.format(nn, ll, v[0]))
            lines.extend(print_help(nn + '_total', self.desc, self.metricType))
            lines.append('{}_total{} {}'.format(nn, ll, v[1]))

        return lines
