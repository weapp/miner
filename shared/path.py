class Path:
    def __init__(self, path, sep="."):
        self.raw_path = path
        self.path = path.split(sep)

    def navigate(self, value):
        for k in self.path:
            if k in value:
                value = value[k]
            else:
                return None
        return value

    def __str__(self):
        return "<Path %s>" % self.raw_path
