#!/usr/bin/env python

from regex_filter import RegexFilter
import re

import lib.grok_patterns as gp

from dateutil import parser as date_time_parser

from datetime import datetime, tzinfo, timedelta

class NginxFilter(RegexFilter):

    def __init__(self, conf):
        RegexFilter.__init__(self, conf)
        self.i = 4

    def filter(self, message):
        self.regexps = [
            # {"regex": """^(?P<ip>.+) (?P<domain>.+) - - \[(?P<nginx_timestamp>.+)] "(?P<verb>.+?) (?P<path>.+?) (?P<http_version>.+?)" (?P<status>.+?) (?P<body_bytes_sent>.+?) "(?P<http_referer>.+?)" "(?P<user_agent>.+) Completed in:(?P<nginx_response_time>.+)"""},
            {"regex": """^(?P<ip>.+) (?P<domain>.+) - - \[%s] "(?P<verb>.+?) (?P<path>.+?) (?P<http_version>.+?)" (?P<status>.+?) (?P<body_bytes_sent>.+?) "(?P<http_referer>.+?)" "(?P<user_agent>.+) Completed in:(?P<nginx_response_time>.+)""" % gp.HTTPDATE_},
        ]

        fields = message.setdefault("fields", {})
        for d in self.parse(message["message"]):
            self.add_fields(fields, self.compact_field_value(d))
        
        fields["timestamp"] = gp.extract_HTTPDATE(fields)

        yield message

