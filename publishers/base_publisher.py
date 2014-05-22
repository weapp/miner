#!/usr/bin/env python

class BasePublisher:
    def __init__(self, conf):
        pass

    def publish(self, message):
        pass

    def __call__(self, message):
        self.publish(message)

    def close(self):
        pass
