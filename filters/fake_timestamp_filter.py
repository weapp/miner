#!/usr/bin/env python
import json
from base_filter import BaseFilter

class FakeTimestampFilter(BaseFilter):
    def filter(self, message):
        if "@fields" in message and "timestamp" in message["@fields"]:
            message["@timestamp"] = message["@fields"]["timestamp"]
        yield message
