from shared.query import Query

class BaseComponent:
    def __init__(self, conf):
        self.conf = conf
        self.query = Query(self.conf.get("query", {}))

    def filter(self, message):
        pass

    def __call__(self, message):
        return self.filter(message)
