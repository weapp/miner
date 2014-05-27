from shared.query import Query
from shared.project import Project

class BaseComponent:
    def __init__(self, conf):
        self.conf = conf or {}
        self.query = Query(self.conf.get("query", {}))
        self.project = Project(self.conf.get("project"))

    def filter(self, message):
        pass

    def __call__(self, message):
        return self.filter(message)
