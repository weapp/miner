from shared.base_component import BaseComponent

class BasePublisher(BaseComponent):
    def __init__(self, conf):
        BaseComponent.__init__(self, conf)

    def publish(self, message):
        pass

    def __call__(self, message):
        if self.query.match(message):
            self.publish(message)

    def close(self):
        pass
