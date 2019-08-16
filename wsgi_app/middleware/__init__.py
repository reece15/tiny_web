# coding:utf-8
import importlib

class BaseMiddleware(object):

    def __init__(self):

        pass

    def process_request(self, request):
        pass

    def process_response(self, request, response):
        return response



def load_middleware():
    import settings

    for item in settings.MIDDLEWARES:
        # FIXME 路径找不到
        index = item.rfind(".")
        middleware_module =importlib.import_module(item[:index])
        middleware = getattr(middleware_module, item[index+1:])
        yield middleware()
