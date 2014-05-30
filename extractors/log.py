#!/usr/bin/env python
from sh import tail, touch, stat, ssh
import re
import time

from base_extractor import BaseExtractor
from shared.utils import build_component
from shared.hash_builder import HashBuilder

class Log(BaseExtractor):
    def extract(self, conf):
        merge = conf.get("should_line_merge", False)
        before = conf.get("break_only_before", None)
        if merge:
            before = re.compile(before)
        
        value = HashBuilder({
                "type": conf.get("type", "log"),
                "source_path": conf["path"],
                "tags": conf.get("tags", [])
            })

        if conf.get("host"):
            host = "%s@%s" % (conf["user"], conf["host"]) if conf.get("user") else conf["host"]
            remote_server = ssh.bake(host)
            mac = str(ssh(host, "ifconfig | grep 'eth0'"))
            value.shared["source_host"] = host
            value.shared["source_mac"] = re.findall("..:..:..:..:..:..", mac)[0]
            log = remote_server.tail("-f", conf["path"], _iter=True)
        else:
            touch(conf["path"])
            if conf.get("from", None) == "now":
                filesize = "-c0"
            else:
                filesize = "-c%s" % (int(stat("-nf" ,'%z', conf["path"])) * 2 + 10)
            log = tail("-F", filesize, conf["path"], _iter=True)

        for n, line in enumerate(log):
            if merge:
                if before.match(line):
                    if value.has_data():
                        yield value.dict()
                        # time.sleep(0.1)
                    value.build()
                value.log(line)
            else:
                value.build(line)
                yield value.dict()
                # time.sleep(0.1)
