# coding:utf-8

import os
import re
import string
import settings


class BaseResponse(object):

    def __init__(self):
        self.status = 200
        self.headers = {}
        self.cookie = []
        self._data = []

    @property
    def status_str(self):
        return "{} {}".format(self.status,"OK" if self.status == 200 else "Internal Server Error")

    @property
    def headers_list(self):
        return list(self.headers.items())

    def add_headers(self, kv_headers):
        self.headers.update(kv_headers or {})

    def __iter__(self):
        for index, item in enumerate(self._data):
            if isinstance(item, str):
                self._data[index] = item.encode("utf-8")

        return iter(self._data)

    def render(self):
        pass


class HtmlResponse(BaseResponse):

    def __init__(self, plain, view_data):
        super(HtmlResponse, self).__init__()
        self._data.append(plain)
        self.add_headers({
            "Content-type": "text/html"
        })
        self.view_data = view_data
        self.render()

    def render(self):
        for index, item in enumerate(self._data):
            self._data[index] = string.Template(item).safe_substitute(self.view_data)


class HtmlFileResponse(HtmlResponse):
    def __init__(self, file_path, view_data):
        plain = None
        for item in settings.TEMPLATE_DIR:
            p = os.path.join(item, file_path)
            if os.path.exists(p):
                with open(p, "rt") as f:
                    plain = f.read()
        if not plain:
            raise FileExistsError(u"template not found in {}".format(settings.TEMPLATE_DIR))
        super(HtmlFileResponse, self).__init__(plain, view_data)


class Http404Error(HtmlResponse):
    def __init__(self):
        plain = '<html><BODY><h1>404 not found!</h1></BODY></html>'
        self.status = 404
        self.view_data = {}
        super(Http404Error, self).__init__(plain=plain, view_data={})


class HTTPResponse(BaseResponse):
    def __init__(self, plain, content_type):
        super(BaseResponse, self).__init__()
        self._data.append(plain)
        self.add_headers({
            "Content-type": content_type
        })
