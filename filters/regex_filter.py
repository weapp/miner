#!/usr/bin/env python

from base_filter import BaseFilter
import re

class RegexFilter(BaseFilter):

    def __init__(self, conf):
        self.regexps = []
        self.compiled = False

    def compile(self, force=False):
        if not self.compiled or force:
            for regex in self.regexps:
                regex["regexc"] = re.compile(regex["regex"])

    def parse(self, message):
        if not self.compiled:
            self.compile()
        return [(m.groupdict() or m.groups()) for regex in self.regexps for m in regex["regexc"].finditer(message)]


    def compact_field_value(self, dict_):
        if "field" in dict_:
            for v in [dict_.pop(k, None) for k in ["value", "value1", "value2"]]:
                if not v is None:
                    dict_[dict_.pop("field")] = v
                    return dict_
        return dict_


    def add_fields(self, one, other):
        for k, v in other.iteritems():
            if k in one:
                if not isinstance(one[k], list):
                    one[k] = [one[k]]
                one[k] = one[k] + v if isinstance(v, list) else one[k] + [v]
            else:
                one[k] = v
        return one
