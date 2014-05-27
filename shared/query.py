from shared.path import Path

class Query:
    def __init__(self, query):
        self.query = query or {}

    def match(self, message):
        r = True
        for k, v in self.query.iteritems():
            k = Path(k)
            r = r and self.check(k.navigate(message), v)
        return r

    def check(self, left, right):
        if isinstance(left, list):
            return right in left
        else:
            return left == right
