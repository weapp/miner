from datetime import datetime, tzinfo, timedelta
import re
import os

patterns = {}


groks = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "grok-patterns")).readlines()
groks = [line.strip().split(" ", 1) for line in groks if line.strip() and not line.startswith("#")]
groks = {k:v for k, v in groks}

def get_pattern(matchobj):
    key = matchobj.group(1).split(":")[0]
    patt = groks.get(key)
    return complete_pattern(patt)

def get_pattern_(matchobj):
    key = matchobj.group(1).split(":")[0]
    patt = groks.get(key)
    patt = "(?P<%s>%s)" % (key, patt)
    return complete_pattern(patt)


def complete_pattern(pattern):
    return re.sub('%{(.+?)}', get_pattern, pattern).replace("(?>","(?:")

def complete_pattern_(pattern):
    return re.sub('%{(.+?)}', get_pattern_, pattern).replace("(?>","(?:")

def month_to_number(month):
    months = "jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec".split("|")
    return months.index(month[:3].lower()) + 1


for key, pattern in groks.iteritems():
    patt = complete_pattern(pattern)
    patterns[key] = patt
    locals()[key] = patt
    
    patt_ = complete_pattern_(pattern)
    patt = "(?P<%s>%s)" % (key, patt_)
    key = "%s_" % key
    patterns[key] = patt
    locals()[key] = patt


def extract_HTTPDATE(fields):
    if "HTTPDATE" in fields:
        fields.pop("HTTPDATE")
        offset = int(fields.pop("INT"))
        month = month_to_number(fields.pop("MONTH"))
        monthday = int(fields.pop("MONTHDAY"))
        time = [int(i) for i in fields.pop("TIME").split(":")]
        year = int(fields.pop("YEAR"))

        class TZ(tzinfo):
            def utcoffset(self, dt):
                return timedelta(hours=offset) + self.dst(dt)
            
            def dst(self, dt):
                return timedelta(hours=offset)

            def tzname(self, dt):
                return "GMT %s" % offset

            def __repr__(self):
                return self.tzname(None)
        
        return datetime(year, month, monthday, time[0], time[1], time[2], tzinfo=TZ()).strftime("%Y-%m-%dT%H:%M:%S.000Z")
