
import platform
from uuid import getnode
import datetime
from objectid import ObjectId
import time

def get_mac():
    mac = hex(getnode())[2:]
    return ("%s:%s:%s:%s:%s:%s" % (
            mac[0:2],
            mac[2:4],
            mac[4:6],
            mac[6:8],
            mac[8:10],
            mac[10:12])).upper()

class HashBuilder:
    def __init__(self, shared, **opts):
        self.shared = {
            "source_mac" : get_mac(),
            "source_host" : platform.node()
        }
        self.shared.update(shared)
        self.fake_timestamp = opts.get("fake_timestamp", False)
        self.build()

    def build(self, data=None):
        self.data = self.shared.copy()
        self.data.setdefault("timestamp", '{0}{1:+06.2f}'.format(datetime.datetime.now().isoformat(), float(time.timezone) / 3600))
        if data is not None:
            self.data["message"] = data

    def log(self, value):
        self.data.setdefault("message", []).append(unicode(value))

    def dict(self):
        if "message" in self.data:
            if isinstance(self.data["message"], list):
                self.data["message"] = "".join(self.data["message"])
            elif isinstance(self.data["message"], dict):
                self.data["fields"] = self.data["message"]
                del self.data["message"]
        return self.data

    def has_data(self):
        return bool(self.data)
