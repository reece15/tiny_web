# coding: utf-8


class Session(object):

    def __init__(self, key, session_id):
        self.session_id = session_id
        self.key = key

    def remove(self, response):
        pass

    def refresh(self, response):
        pass

    def is_exp(self):
        pass

    def is_alive(self):
        pass

    def get(self):
        pass

    def set(self, val):
        pass
