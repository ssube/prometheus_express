class CollectorRegistry():
    metrics = []
    namespace = ''
    path = ''

    def __init__(self, metrics=[], namespace='', path='/metrics'):
        self.metrics = set(metrics)
        self.namespace = namespace
        self.path = path

    def register(self, metric):
        if metric in self.metrics:
            return True

        self.metrics.add(metric)
        return True

    def print(self):
        metrics = []
        for m in self.metrics:
            line = m.print(self.namespace)
            metrics.extend(line)

        return metrics
