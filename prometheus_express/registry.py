exposition_line = '\n'

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

    def render(self):
        metrics = []
        for m in self.metrics:
            line = m.render(self.namespace)
            metrics.extend(line)

        return metrics

    def handler(self, headers, body):
        return {
            'status': '200 OK',
            'content': exposition_line.join(self.render()),
        }