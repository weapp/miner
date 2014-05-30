#!/usr/bin/env python
from base_filter import BaseFilter
import pygeoip
import os

gi = pygeoip.GeoIP(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'GeoLiteCity.dat'))


class GeoipFilter(BaseFilter):
    def filter(self, message):
        message["fields"]["geoip"] = gi.record_by_addr(message["fields"]["ip"])
        yield message
