#!/usr/bin/env python
import yaml
import json
from pprint import pprint

from pygments.lexers import JadeLexer
from pygments.lexers import JSONLexer
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
from pygments import highlight

from base_publisher import BasePublisher

from termcolor import colored, COLORS


def pp(message, indent=0):
    print pformat(message, indent)

def pformat(message, indent=0):
    if isinstance(message, dict):
        r = []
        for k, v in sorted(message.iteritems()):
            key = "%s%s:" % ("  " * indent, colored(k, 'green'))
            value = pformat(v, indent + 1)
            if "\n" in value:
                r.append(key)
                r.append(value)
            else:
                r.append("%s %s" % (key, value.lstrip()))
        return "\n".join(r)
    elif isinstance(message, basestring):    
        if "\n" in message:
            return "%s%s" % ("  " * indent, colored(repr(message), 'magenta'))
        else:
            return "%s%s" % ("  " * indent, colored(message, 'magenta'))
    elif isinstance(message, (int, long, complex)):    
        return "%s%s" % ("  " * indent, colored(message, 'red'))
    elif isinstance(message, float):    
        return "%s%s" % ("  " * indent, colored("%.2f" % message, 'red'))
    elif isinstance(message, (list, tuple)):    
        mess = [pformat(v, indent + 1) for v in message]
        n = any(True for m in mess if "\n" in m)
        if n:
            r = []
            r.append("%s%s" % ("  " * indent, "["))

            inside = []
            for m in mess:
                inside.append("%s%s" % ("", m))

            r.append(("\n%s,\n" % ("  " * (indent+1))).join(inside))
            r.append("%s%s" % ("  " * indent, "]"))
            return "\n".join(r)
        else:
            return "[%s]" % ", ".join([m.lstrip() for m in mess])
    else:
        return "%s%s" % ("  " * indent, repr(message)) 

class PrintPublisher(BasePublisher):
    def publish(self, message):
        # # pprint(message)
        # # message = json.dumps(message, sort_keys=True, indent=2)
        # message2 = yaml.dump(message, default_flow_style=False)
        # print highlight(message2, JadeLexer(), TerminalFormatter())
        # message2 = json.dumps(message, sort_keys=True, indent=2)
        # print highlight(message2, JSONLexer(), TerminalFormatter())
        # print


        pp(message)
        print
        print
        
