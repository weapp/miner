from shared.base_component import BaseComponent

class BaseFilter(BaseComponent):
    def __init__(self, conf):
        BaseComponent.__init__(self, conf)

    def filter(self, message):
        pass

    def __call__(self, message):
        return self.filter(message)
