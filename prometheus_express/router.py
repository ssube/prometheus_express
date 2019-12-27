def response(content, status='200 OK'):
    return {
        'status': status,
        'content': content,
    }

def errorHandler(headers, body):
    return response('Not Found', '404 Not Found')

class Router():
    def __init__(self):
        self.routes = []

    def __contains__(self, route):
        for r in self.routes:
            if r[0] == route[0] and r[1] == route[1]:
                return r[2]

    def __iter__(self):
        return self.routes.__iter__()

    def __len__(self):
        return self.routes.__len__()

    def register(self, method, path, handler):
        self.routes.append((method, path, handler))

    def select(self, method, path):
        for r in self.routes:
            if r[0] == method and r[1] == path:
                return r[2]

        return errorHandler
