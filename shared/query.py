from shared.path import Path
from copy import deepcopy

class Checker:
    def __init__(self, value):
        self.value = value

    def _check(self, other):
        value = deepcopy(self.value)
        ret = True
        if isinstance(value, dict):
            if "$lt" in value:
                ret and other < value.pop("$lt")
            if "$gt" in value:
                ret = ret and other > value.pop("$gt")
            if "$lte" in value:
                ret = ret and other <= value.pop("$lte")
            if "$gte" in value:
                ret = ret and other >= value.pop("$gte")
            if "$ne" in value:
                ret = ret and other != value.pop("$ne")
            if "$in" in value:
                ret = ret and other in value.pop("$in")
            if "$nin" in value:
                ret = ret and other not in value.pop("$nin")
        if value:
            ret = ret and value == other
        return ret

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
