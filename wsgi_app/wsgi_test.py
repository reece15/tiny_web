# coding: utf-8

from wsgiref.simple_server import make_server

def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello World'.encode("utf-8")]

def get_env_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    s = []
    for k, v in environ.items():
        s.append("key:{} val:{}\n".format(k, v).encode("utf-8"))
    return s


"""
url路径     PATH_INFO
提交的参数  QUERY_STRING 
请求方式    REQUEST_METHOD

"""

srv = make_server('localhost', 9797, get_env_app)
print("runing!")
srv.serve_forever()