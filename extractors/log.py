#!/usr/bin/env python
from base_extractor import BaseExtractor
from lib.utils import build_component, HashBuilder
from sh import tail, touch, stat
import re

class Log(BaseExtractor):
    def extract(self, conf):
        merge = conf.get("should_line_merge", False)
        before = conf.get("break_only_before", None)
        if merge:
            before = re.compile(before)

        value = HashBuilder({"@type": conf.get("type", "log"),"@source_path": conf["path"], "@tags": conf.get("tags", [])}, fake_timestamp=conf["fake_timestamp"])

        touch(conf["path"])

        filesize = "-c%s" % (int(stat("-nf" ,'%z', conf["path"])) * 2 + 10)

        for n, line in enumerate(tail("-F", filesize, conf["path"], _iter=True)):
            if merge:
                if before.match(line):
                    if value.has_data():
                        yield value.dict()
                    value.build()
                value.log(line)
            else:
                value.build(line)
                yield value.dict()
