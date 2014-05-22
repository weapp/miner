#!/usr/bin/env python

from regex_filter import RegexFilter
import re
from pprint import pprint


class RailsFilter(RegexFilter):

    def __init__(self, conf):
        RegexFilter.__init__(self, conf)

    def filter(self, message):
        self.regexps = [
            {"regex": """(?P<ip>(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))"""},
            {"regex": """^Started (?P<verb>\w+) \"(?P<url>[^"]+)\""""},
            {"regex": """Completed (?P<status>\S+) .*? in (?P<completed_time>\d+\.?\d*ms)"""},
            {"regex": """Processing by (?P<controller>\S+)#(?P<action>\S+)"""},
            {"regex": """Rendered (?P<template>\S+) within (?P<template_time>\S+)"""},
            {"regex": """\d\d\d\d/\d\d/\d\d \d\d:\d\d:\d\d \[(?P<status>\w+)\]"""},
            {"regex": """(?P<timestamp>\d\d\d\d[\-\/]\d\d[\-\/]\d\d \d\d:\d\d:\d\d(?: \+\d\d\d\d)?)"""},
            {"regex": """(?P<field>\w+)=(?P<value>[^\s"&]*)"""},
            {"regex": """(?P<field>[A-Za-z]\w*):\s(?P<value2>([^"\s,]+)|"([^\"]*)")"""},
            {"regex": """^(?P<ip>.+) (?P<domain>.+) - - \[(?P<nginx_timestamp>.+)] "(?P<verb>.+?) (?P<path>.+?) (?P<http_version>.+?)" (?P<status>.+?) (?P<body_bytes_sent>.+?) "(?P<http_referer>.+?)" "(?P<user_agent>.+) Completed in:(?P<nginx_response_time>.+)"""},
        ]


        fields = message.setdefault("@fields", {})
        for d in self.parse(message["@message"]):
            self.add_fields(fields, self.compact_field_value(d))

        yield message
