#!/usr/bin/env python
from elasticsearch import Elasticsearch
from shared.objectid import ObjectId
from pprint import pprint

import logging

from base_publisher import BasePublisher

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.WARNING)
    
class ElasticPublisher(BasePublisher):
    def __init__(self, conf):
        self.es = Elasticsearch()

    def publish(self, message):
        id_ = message.pop("_id", None) or str(ObjectId())
        id_ = int(id_, 16)

        message["_score"] = 1
        message["message"] = message.pop("message", "")
        message["version"] = 1
        message["host"] = message.pop("source_host", "")

        
        index = "logstash-%s" % message["timestamp"][0:10].replace("-",".")

        # print "-" * 40
        # pprint (id_)
        # pprint (message)
        # print "-" * 40

        self.es.index(index=index, doc_type="logs", id=id_, body=message)
