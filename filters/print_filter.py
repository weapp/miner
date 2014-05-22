#!/usr/bin/env python
import json

from pygments.lexers import JSONLexer
from pygments.formatters import TerminalFormatter
from pygments import highlight

from base_filter import BaseFilter


class PrintFilter(BaseFilter):
    def filter(self, message):
        message2 = json.dumps(message, sort_keys=True, indent=2)
        print highlight(message2, JSONLexer(), TerminalFormatter())
        print
        yield message
