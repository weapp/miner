#!/usr/bin/env python
from base_extractor import BaseExtractor
from shared.utils import HashBuilder
import time

class Execute(BaseExtractor):
    def extract(self, conf):
        value = HashBuilder({"@type": conf.get("type", "exec"),"@tags": conf.get("tags", [])})
        if "init" in conf:
            exec(conf["init"])
        while 1:
            init = time.time()
            if "exec" in conf:
                exec(conf["exec"])
            if "eval" in conf:
                value.build(eval(conf["eval"]))
            yield value.dict()

            time.sleep(max(init + conf.get("interval", 1) - time.time(), 0))
