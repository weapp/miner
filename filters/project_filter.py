#!/usr/bin/env python
from base_filter import BaseFilter
from shared.project import Project

class ProjectFilter(BaseFilter):
    def __init__(self, conf):
        BaseFilter.__init__(self, conf)

    def filter(self, message):
        yield self.project.transform(message)
