# coding: utf-8
import os

BASE_PATH = os.path.dirname(__file__)

TEMPLATE_DIR = (
    os.path.join(BASE_PATH, "templates/"),
)

VIEWS_FILES = (
    "views",
)

MIDDLEWARES = (
    "wsgi_app.middleware.session_middleware.SessionMiddleware",
)


COOKIES_BACKEND = "wsgi_app.session.session_file.FileSession"