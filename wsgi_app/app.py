# coding: utf-8

from wsgiref.simple_server import make_server
from router.routers import Router
from http_process.request import Request
from middleware import load_middleware

class BaseWSGIApp(object):
    def __call__(self, environ, start_response):

        # 处理并生成request对象 处理GET POST 请求参数
        middleware = list(load_middleware())

        request = self.process_request(environ)

        for item in middleware:
            item.process_request(request)

        # 路由，然后处理中间件和业务逻辑
        response = self.process_response(request)

        for item in reversed(middleware):
            res = item.process_response(request, response)
            if res:
                response = res
            else:
                break

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
        # TODO 中间件
        # TODO 开始处理请求事件/切面
        return Router.routing(request)


def run(ip="localhost", port=9797):
    srv = make_server(ip, port, WSGIApp())
    print("runing in {}:{}!".format(ip, port))
    srv.serve_forever()
