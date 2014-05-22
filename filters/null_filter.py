#!/usr/bin/env python

from base_filter import BaseFilter


class NullFilter(BaseFilter):
    def filter(self, message):
        exit(1)
        if None:
            yield None
