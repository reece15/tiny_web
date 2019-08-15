# coding: utf-8
import re
from urllib.parse import unquote

class BaseRequest(object):

    def __init__(self, env):
        self.env = env
        self.query = env.get("QUERY_STRING")
        self.path = env.get("PATH_INFO")
        self.method = env.get("REQUEST_METHOD")
        self.content_length = int(env.get("CONTENT_LENGTH", 0) or 0)
        self.GET = {}
        if self.query:
            self.GET.update(self.parse_query(self.query))
        if self.method == "POST":
            self.POST = {}
            data = self.env['wsgi.input'].read(self.content_length)

            self.POST.update(self.parse_query(data))
            print(self.POST)

        print(self.GET)


    def parse_query(self, data):
        if isinstance(data, bytes):
            data = data.decode("utf-8")
        res = {}
        print(data, type(data))
        for item in unquote(data).split("&"):
            m = re.match(r"([^=]+)=(.*)", item)
            if m:
                k = m.group(1)
                v = m.group(2)
                if k.endswith("[]"):
                    k = k[:-2]
                    if k not in res:
                        res[k] = []
                    res[k].append(v)
                else:
                    res[k] = v

        return res

class Request(BaseRequest):
    def __init__(self, env):
        super(Request, self).__init__(env)
