#!/usr/bin/env python
from base_filter import BaseFilter
from shared.query import Query

class SelectFilter(BaseFilter):
    def __init__(self, conf):
        BaseFilter.__init__(self, conf)

    def filter(self, message):
        if self.query.match(message):
            yield message
