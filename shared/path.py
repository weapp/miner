class Path:
    def __init__(self, path):
        self.raw_path = path
        self.path = path.split("/")

    def navigate(self, value):
        for k in self.path:
            if k in value:
                value = value[k]
            else:
                return None
        return value
