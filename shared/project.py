from shared.path import Path
from copy import deepcopy

class Project:
    def __init__(self, project):
        self.project = project or None

    def _transform(self, ret, message):
        if isinstance(ret, basestring) and ret.startswith("$"):
            ret = Path(ret[1:]).navigate(message)
        elif isinstance(ret, list):
            ret = [self._transform(r, message) for r in ret]
        elif isinstance(ret, dict):
            if ret.pop("$meta", False):
                for k in ["tags", "type", "timestamp", "source_mac", "source_host"]:
                    ret[k] = message[k]
            reject_none = ret.pop("$rejectNone", False)
            for k in ret.keys():
                v = self._transform(ret[k], message)
                if reject_none and v is None:
                    del ret[k]
                else:
                    ret[k] = v
        return ret


    def transform(self, message):
        if self.project is None:
            return message

        return self._transform(deepcopy(self.project), message)
