from prometheus_express.router import response

exposition_break = '\n'

def name_sort(metric):
    return metric.name

class CollectorRegistry():
    metrics = []
    namespace = ''
    path = ''

    def __init__(self, metrics=[], namespace=''):
        self.metrics = set(metrics)
        self.namespace = namespace

    def register(self, metric):
        if metric in self.metrics:
            return True

        self.metrics.add(metric)
        return True

    def render(self, sorted=False):
        if sorted:
            metrics = sorted(self.metrics, key=name_sort)
        else:
            metrics = self.metrics

        output = []
        for m in metrics:
            output.extend(m.render(self.namespace))

        return output

    def handler(self, headers, body):
        return response(exposition_break.join(self.render()))