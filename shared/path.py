class Path:
    def __init__(self, path, sep="."):
        self.raw_path = path
        self.path = path.split(sep)

    def navigate(self, value):
        for k in self.path:
            if k in value:
                value = value[k]
            elif k == "$last":
                value = value[-1]
            elif k == "$first":
                value = value[0]
            else:
                return None
        return value

    def __str__(self):
        return "<Path %s>" % self.raw_path
