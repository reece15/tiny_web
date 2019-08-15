# coding: utf-8
from wsgi_app.http_process.response import HtmlFileResponse
from wsgi_app.router.routers import Router

@Router.reg(path="^/index$")
def index(request):
    name = ""
    if request.method == "GET":
        name = request.GET.get("name")
    else:
        name = request.POST.get("name")
    return HtmlFileResponse("index.html", {"user_name": name})