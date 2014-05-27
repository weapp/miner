#!/usr/bin/env python
from shared.utils import build_components

class BaseExtractor:
    def __init__(self, conf):
        self.conf = conf

    def extract(self, conf):
        if None:
            yield None

    def __call__(self, publishers):
        return dict(target=self.make_reader, args=(self.conf, publishers))


    def make_reader(self, conf, publishers):    
        filters = build_components(conf, "filters")
        for value in self.extract(conf):
            values = [value]
            for filter_ in filters:
                values = [value for value_ in values for value in filter_(value_)]
            for value in values:
                self.publish(publishers, value)

    def publish(self, publishers, value):
        [publisher(value) for publisher in publishers]
