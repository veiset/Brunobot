import api.base

class Manager():

    def __init__(self):
        self.api = {}


    def add(self, name, api):
        self.api[name] = api.base.SimpleAPI()
