# coding: utf-8
import importlib
from . import BaseMiddleware
from wsgi_app.session.session_file import FileSession

import settings

SESSION_KEY = "psessionid"

class SessionMiddleware(BaseMiddleware):

    def __init__(self):
        super(SessionMiddleware, self).__init__()
        index = settings.COOKIES_BACKEND.rfind(".")
        m = settings.COOKIES_BACKEND[:index]
        s = settings.COOKIES_BACKEND[index + 1:]
        module = importlib.import_module(m)
        self.session_backend = getattr(module, s)

    def process_request(self, request):
        """
        根据session_id找文件
        :param request:
        :return:
        """

        cookies = request.cookies
        sessoion_id = cookies.get(SESSION_KEY)
        s = self.session_backend(SESSION_KEY, sessoion_id)
        self.patch_session(s, request)

    def process_response(self, request, response):
        """
        如果没有session_id的话 生成
        :param request:
        :param response:
        :return:
        """
        cookies = request.cookies
        sessoion_id = cookies.get(SESSION_KEY)
        if not sessoion_id:
            s = self.session_backend(SESSION_KEY, sessoion_id)
            s.re_new(response)
        return response


    def patch_session(self, s, request):
        request.session = s