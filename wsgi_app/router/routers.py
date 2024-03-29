# coding:utf-8
import re
import settings
import importlib
from router.sign import router_views
from http_process.response import Http404Error


class Router(object):
    @staticmethod
    def reg(path):
        """
        绑定url和method
        :param path:
        :return:
        """
        def f(func):
            router_views[path] = func
            return func
        return f

    @staticmethod
    def routing(request):
        """
        路由 url--->method
        :param request: 请求对象
        :return: response 对象
        """
        if not router_views:
            for item in settings.VIEWS_FILES:
                views = importlib.import_module(item)
                importlib.reload(views)

        for p, func in router_views.items():
            if re.match(p, request.path):
                return func(request)

        return Http404Error()  # 404 ERROR
