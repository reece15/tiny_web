# coding:utf-8
import re
import settings
import importlib
from router.sign import router_views
from http_process.response import Http404Error

class Router(object):
    @staticmethod
    def reg(path):
        def f(func):
            router_views[path] = func
            print("hit",router_views)
            return func
        return f

    @staticmethod
    def routing(request):
        print("test1", router_views)
        if not router_views:
            for item in settings.VIEWS_FILES:
                views = importlib.import_module(item)
                print("reload hit!")
                importlib.reload(views)

        print("test",router_views)
        for p, func in router_views.items():
            print(p,func)
            if re.match(p, request.path):
                return func(request)

        return Http404Error() # FIXME 404 ERROR