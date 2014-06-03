from base_publisher import BasePublisher
from pprint import pprint as pp
from wu_client import WuClient
from shared.path import Path


class WubytesPublisher(BasePublisher):
    def __init__(self, conf):
        BasePublisher.__init__(self, conf)

        self.wc = WuClient(conf["client_id"], conf["client_secret"], conf["host"])
        if not self.wc.auth(conf["username"], conf["pass"]):
            exit()

        for key in self.project.project:
            self.wc.new_wu({'data': 0, 'title': key, 'slug': key})

    def publish(self, message):
        for key, value in message.iteritems():
            print key, value
            self.wc.update_value(key, value)
