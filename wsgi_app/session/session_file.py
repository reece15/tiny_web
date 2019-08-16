# coding: utf-8
import json
import datetime
import os
import time
from . import Session
import tempfile
import uuid
from functools import lru_cache

class FileSession(Session):

    def __init__(self, key, session_id):
        super(FileSession, self).__init__(key=key, session_id=session_id)
        self.file_path = "w_cookie"
        self.dir = self.get_coolie_dir()

        self.file = None
        if self.session_id:
            self.file = os.path.join(self.dir, self.session_id)

        self.times = 3600
        self.val = self.get()

    def get_coolie_dir(self):
        d = os.path.join(tempfile.gettempdir(), self.file_path)
        if not os.path.exists(d):
            os.makedirs(d)
        return d

    def remove(self, response):
        os.remove(self.file)
        self.refresh(response)

    def refresh(self, response):
        response.add_headers({
            "Set-Cookie": "{}={}; Expires={}; Domain={}; Path={}".format(self.key, self.session_id,
                                                                         datetime.datetime.utcfromtimestamp(
                                                                             self.get_exp()).strftime(
                                                                             "%a, %d-%b-%Y %T GMT"), "", "/")
        })

    def re_new(self, response):
        session_id = str(uuid.uuid1()).replace("-","")  # FIXME session_id生成不安全也过于简单
        self.session_id = session_id
        self.file = os.path.join(self.dir, self.session_id)
        # self.set(0) 没有登录的暂时不需要存session
        self.refresh(response)

    def get(self): # FIXME 先缓存  再读文件
        if not self.session_id:
            return None
        return get_from_file(self.file)

    def get_exp(self):
        return time.time()+ self.times

    def set(self, val):
        if not isinstance(val, str):
            val = str(val)
        with open(self.file, "w") as f:
            f.write(json.dumps({
                "val":val,
                "time": self.get_exp()
            }))


def get_from_file(file):
    if not os.path.exists(file):
        return None
    with open(file, "r") as f:
        return json.loads(f.read())