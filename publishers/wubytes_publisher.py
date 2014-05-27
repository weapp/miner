from base_publisher import BasePublisher
from pprint import pprint as pp
from wu_client import WuClient
from shared.path import Path

def get_password(conf):
    password = conf.get("pass", None) or conf.get("password", None)
    if not password:
        print "Password for wubytes:",
        password = raw_input().strip()
    return password

class WubytesPublisher(BasePublisher):
    def __init__(self, conf):

        self.keys = conf["keys"]

        self.wc = WuClient(conf["client_id"], conf["client_secret"], conf["host"])
        if not self.wc.auth(conf["username"], get_password(conf)):
            exit()

        for key in self.keys:
            self.wc.new_wu({'data': 0, 'title': key, 'slug': key})

    def publish(self, message):
        try:
            for key, path in self.keys.iteritems():
                path = Path(path)
                value = path.navigate(message)
                print key, path, value
                self.wc.update_value(key, value)
        except KeyError:
            pass
