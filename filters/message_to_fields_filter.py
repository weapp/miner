#!/usr/bin/env python

from base_filter import BaseFilter


class MessageToFieldsFilter(BaseFilter):
    def filter(self, message):
        message["fields"] = message.pop("message", {})
        yield message
