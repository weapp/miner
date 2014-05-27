from shared.path import Path

class Checker:
    def __init__(self, value):
        self.value = value

    def _check(self, other):
        if isinstance(self.value, dict):
            if "$lt" in self.value:
                return other < self.value["$lt"]
            if "$gt" in self.value:
                return other > self.value["$gt"]
            if "$lte" in self.value:
                return other <= self.value["$lte"]
            if "$gte" in self.value:
                return other >= self.value["$gte"]
        return self.value == other

    def check(self, other):
        if isinstance(other, list):
            return any(self._check(o) for o in other)
        else:
            return self._check(other)

class Query:
    def __init__(self, query):
        self.raw_query = query or {}
        self.query = {Path(k):Checker(v) for k, v in self.raw_query.iteritems()}

    def match(self, message):
        r = True
        for path, checker in self.query.iteritems():
            r = r and checker.check(path.navigate(message))
        return r
