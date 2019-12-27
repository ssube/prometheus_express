def render_help(name, desc, type):
    return [
        '# HELP {} {}'.format(name, desc),
        '# TYPE {} {}'.format(name, type),
    ]


def render_labels(keys, values):
    if len(keys) != len(values):
        raise ValueError('length of label values must equal label keys')

    if len(keys) == 0:
        return ''

    labels = []
    for k, v in zip(keys, values):
        labels.append('{}="{}"'.format(k, v))

    return '{' + ','.join(labels) + '}'


def render_name(namespace, name):
    if namespace != '':
        return '{}_{}'.format(namespace, name)
    else:
        return name

def is_alpha(c):
    return (
        c >= 'a' and c <= 'z' or    # lowercase alpha
        c >= 'A' and c <= 'Z')      # uppercase alpha

def is_numeric(c):
    return (c >= '0' and c <= '9')

'''
Validate a single character. This avoids importing regex on the Express platform.
From https://github.com/prometheus/common/blob/master/model/metric.go#L97
'''
def validate_name_char(c, num):
    return (
        is_alpha(c) or
        (num and is_numeric(c)) or
        c == '_' or
        c == ':')

'''
Validate a metric or label name without using regular expressions.
'''
def validate_name(name):
    head = name[0]
    tail = name[1:]

    return validate_name_char(head, False) and all(
        validate_name_char(c, True) for c in tail
    )

'''
Base class for typed metrics
'''
class Metric(object):
    name = ''
    desc = ''
    labelKeys = []
    metricType = 'untyped'

    def __init__(self, name, desc, labels=[], registry=False):
        if not validate_name(name):
            raise ValueError('metric name is not valid')
        if not all(validate_name(n) for n in labels):
            raise ValueError('label names are not valid')

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

    def labels(self, *labelValues):
        self.labelValues = labelValues
        return self

    def render(self, namespace):
        return render_help(render_name(namespace, self.name), self.desc, self.metricType)


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
            self.values[self.labelValues] = 0 - value

        self.labelValues = self.emptyLabels

    def render(self, namespace):
        lines = super(Counter, self).render(namespace)
        for l, v in self.values.items():
            lines.append('{}{} {}'.format(render_name(
                namespace, self.name), render_labels(self.labelKeys, l), v))

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

        self.labelValues = self.emptyLabels

    def render(self, namespace):
        nn = render_name(namespace, self.name)
        lines = super(Summary, self).render(namespace)
        for l, v in self.values.items():
            ll = render_labels(self.labelKeys, l)
            lines.append('{}_count{} {}'.format(nn, ll, v[0]))
            lines.append('{}_total{} {}'.format(nn, ll, v[1]))

        return lines
