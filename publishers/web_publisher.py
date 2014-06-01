#!/usr/bin/env python
from base_publisher import BasePublisher
from shared.hash_builder import HashBuilder
from shared.utils import parse_time
from shared.project import Project
import time
import urllib, urllib2
import json
from pprint import pprint as pp

class WebPublisher(BasePublisher):

    def __init__(self, conf):
        BasePublisher.__init__(self, conf)
        self.url = self.conf["url"]
        self.verb = self.conf.get("verb", "GET")
        self.json = self.conf.get("json", False)
        self.data = Project(self.conf.get("data"))
        self.opener = urllib2.build_opener()
        
    def publish(self, message):
        #curl -XPOST localhost:4567/id -d '{"wadus":"badus"}'
        # pp(self.opener.open(self.build_request()).read())
        try:
            pp(self.opener.open(self.build_request(message)).read())
        except:
            pass

    def build_request(self, message):
        url = self.url.format(**message)
        if self.data:
            data = self.data.transform(message)
            data = json.dumps(data) if self.json else urllib.urlencode(data)
            request = urllib2.Request(url, data=data)
        else:
            request = urllib2.Request(url)
        
        request.get_method = lambda: self.verb.upper()

        return request
