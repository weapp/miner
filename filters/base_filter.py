#!/usr/bin/env python

class BaseFilter:
    def __init__(self, conf):
        pass

    def filter(self, message):
        pass

    def __call__(self, message):
        return self.filter(message)
