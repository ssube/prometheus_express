from prometheus_express.server import http_default_status


def response(content, status=http_default_status):
    return {
        'status': status,
        'content': content,
    }


def error_handler(headers, body):
    return response('Not Found', '404 Not Found')


def bind_middleware(handler, middleware=[]):
    def invoke(headers, body):
        for m in middleware:
            r = m(headers, body)
            if r != None:
                return r

        return handler(headers, body)

    return invoke


def validate_route(handler):
    return (len(handler) == 3 and
            type(handler[0]) == str and
            type(handler[1]) == str and
            callable(handler[2]))


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

    def _register(self, route):
        if validate_route(route):
            self.routes.append(route)
        else:
            raise ValueError('invalid route')

    def register(self, method, path, handler):
        route = (method, path, handler)
        self._register(route)

    def register_all(self, routes):
        for r in routes:
            self._register(r)

    def select(self, method, path):
        for r in self.routes:
            if r[0] == method and r[1] == path:
                return r[2]

        return error_handler
