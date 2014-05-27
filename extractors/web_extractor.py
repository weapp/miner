#!/usr/bin/env python
from base_extractor import BaseExtractor
from shared.hash_builder import HashBuilder
from shared.utils import parse_time
import time
import urllib, urllib2
import json

class WebExtractor(BaseExtractor):

    def __init__(self, conf):
        BaseExtractor.__init__(self, conf)
        interval = self.conf.get("interval", "1s")
        self.interval = parse_time(interval)
        self.url = self.conf["url"]
        self.verb = self.conf.get("verb", "GET")
        self.json = self.conf.get("json", False)
        self.data = self.conf.get("data")
        self.opener = urllib2.build_opener()
        self.request = self.build_request()
        self.tags = conf.get("tags", [])
        self.tags.append("web")
        if self.json:
            self.tags.append("json")

    def extract(self, conf):
        value = HashBuilder({"type": conf.get("type", "web"),"tags": self.tags})
        while 1:
            init = time.time()
            value.build(self.tick())
            yield value.dict()
            time.sleep(max(init + self.interval - time.time(), 0))

    def tick(self):
        r = self.opener.open(self.request).read()
        if self.json:
            r = json.loads(r)
        return r


    def build_request(self):
        if self.data:
            self.data = urllib.urlencode(self.data)
            request = urllib2.Request(self.url, data=self.data)
        else:
            request = urllib2.Request(self.url)
        
        request.get_method = lambda: self.verb.upper()
        return request


    def _open(self, verb, url, data=None):
        r = self.opener.open(request)
        return json.loads(r.read())

