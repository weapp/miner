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

    def exist(self, value):
        for k in self.path:
            if k in value:
                value = value[k]
            elif k == "$last":
                if value:
                    value = value[-1]
                else:
                    return False
            elif k == "$first":
                if value:
                    value = value[0]
                else:
                    return False
            else:
                return False
        return True

    def __str__(self):
        return "<Path %s>" % self.raw_path
