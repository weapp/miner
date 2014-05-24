from base_publisher import BasePublisher
from pprint import pprint as pp
from wu_client import WuClient

print "password for wubytes:",
password = raw_input().strip()

class WubytesPublisher(BasePublisher):
    def __init__(self, conf):

        self.keys = conf["keys"]

        self.wc = WuClient(conf["client_id"], conf["client_secret"])
        if not self.wc.auth(conf["username"], password):
            exit()

        for key in self.keys:
            self.wc.new_wu({'data': 0, 'title': key, 'slug': key})

    def publish(self, message):

        for key, path in self.keys.iteritems():
            value = message
            for k in path.split("/"):
                value = value[k]


            print key, path, value

            self.wc.update_value(key, value)
            
