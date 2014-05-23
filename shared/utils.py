import re
import platform
from uuid import getnode
import datetime
from objectid import ObjectId
import time


_camel_pat = re.compile(r'([A-Z])')
_under_pat = re.compile(r'_([a-z])')


def camel_to_underscore(name):
    return _camel_pat.sub(lambda x: '_' + x.group(1).lower(), name)[1:]

def underscore_to_camel(name):
    return _under_pat.sub(lambda x: x.group(1).upper(), name.capitalize())


def build_components(conf, key):
    components = conf.get(key, None) or []
    return [build_component(component) for component in components]


def build_component(component):
    if isinstance(component, basestring):
        component = {component:{}}
    for class_, conf in component.items():
        module_class = class_.split(":")
        module_class = class_.split(".")
        route = [camel_to_underscore(c) for c in module_class]
        module_name = route[-1]
        class_name = module_class[-1]
        route = ".".join(route)
        module = __import__(route, globals(), locals(), [module_name])
        class_ =  getattr(module, class_name)
        return class_(conf)



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
            "@source_mac" : get_mac(),
            "@source_host" : platform.node()
        }
        self.shared.update(shared)
        self.fake_timestamp = opts.get("fake_timestamp", False)
        self.build()

    def build(self, data=None):
        self.data = self.shared.copy()
        self.data.setdefault("@timestamp", '{0}{1:+06.2f}'.format(datetime.datetime.now().isoformat(), float(time.timezone) / 3600))
        if data is not None:
            self.data["@message"] = data

    def log(self, value):
        self.data.setdefault("@message", []).append(unicode(value))

    def dict(self):
        if isinstance(self.data["@message"], list):
            self.data["@message"] = "".join(self.data["@message"])
        return self.data

    def has_data(self):
        return bool(self.data)
