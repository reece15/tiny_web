# coding: utf-8

from wsgiref.simple_server import make_server
from router.routers import Router
from http_process.request import Request

class BaseWSGIApp(object):
    def __call__(self, environ, start_response):
        print(environ)
        request = self.process_request(environ)
        response = self.process_response(request)
        start_response(response.status_str, response.headers_list)

        return response

    def process_request(self, env):
        raise NotImplementedError

    def process_response(self, request):
        raise NotImplementedError

class WSGIApp(BaseWSGIApp):

    def process_request(self, env):
        return Request(env)

    def process_response(self, request):
        return Router.routing(request)


def run(ip="localhost", port=9797):
    srv = make_server(ip, port, WSGIApp())
    print("runing in {}:{}!".format(ip, port))
    srv.serve_forever()