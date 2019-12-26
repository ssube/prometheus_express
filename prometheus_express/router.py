def errorHandler(headers, body):
    return {
      'status': 404,
      'content': 'Not Found',
    }


class Router():
    routes = []

    def __init__(self, routes=[]):
        self.routes = routes

    def register(self, method, path, handler):
        self.routes.append((method, path, handler))

    def select(self, method, path):
        for r in self.routes:
            if r[0] == method and r[1] == path:
                return r[2]

        return errorHandler
