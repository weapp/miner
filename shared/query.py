class Query:
    def __init__(self, query):
        self.query = query or {}

    def match(self, message):
        r = True
        for k, v in self.query.iteritems():
            r = r and self.check(self.navigate(message, k), v)
        return r

    def check(self, left, right):
        if isinstance(left, list):
            return right in left
        else:
            return left == right

    def navigate(self, value, path):
        for k in path.split("/"):
            if k in value:
                value = value[k]
            else:
                return None
        return value
