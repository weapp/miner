#!/usr/bin/env python
from base_filter import BaseFilter
from shared.hash_builder import HashBuilder
from shared.query import Query
from shared.path import Path

import time

import re
from math import ceil

import numpy as np


re_retention = re.compile("^(\d+)([ywdhms]):(\d+)([ywdhms])$")
re_d = re.compile("^\s*(\d+(?:.\d+)?)")

to_sec = {
    "s" : 1,
    "m" : 60,
    "h" : 60 * 60,
    "d" : 60 * 60 * 24,
    "w" : 60 * 60 * 24 * 7,
    "y" : 60 * 60 * 24 * 365.5,
}


class Operation:
    def __init__(self, operation):
        self.operation_name = operation
        self.operation = {
            "count": len,
            "avg": self.avg,
            "median": self.median,
            "percentile_95": self.avg,
            "max": self.max,
            "min": self.min,
        }[operation]

    def __call__(self, values):
        return self.operation(values)

    def avg(self, values):
        values = self.float_values(values)
        return sum(values)/len(values)

    def median(self, values):
        return np.percentile(self.float_values(values), 50)

    def percentile_95(self, values):
        return np.percentile(self.float_values(values), 95)

    def max(self, values):
        return max(self.float_values(values))

    def min(self, values):
        return min(self.float_values(values))

    def avg(self, values):
        values = self.float_values(values)
        return sum(values)/len(values)

    def float_values(self, values):
        return [float(re_d.match(v).group(1) or 0) for v in values if v is not None]

class AggregateFilter(BaseFilter):

    def parse_retentions(self, retention):
        delta, delta_unit, persist, persist_unit = re_retention.match(retention).groups()
        delta = int(delta) * to_sec[delta_unit]
        persist = int(persist) * to_sec[persist_unit]

        return (delta, int(ceil(float(persist)/delta)))


    def __init__(self, conf):
        BaseFilter.__init__(self, conf)
        self.query = Query(self.conf.get("query"))
        self.key = Path(self.conf.get("key", "/"))
        self.operation = Operation(self.conf.get("operation", "count"))

        tags = ["generated", "aggregate", self.conf.get("operation")] + self.conf.get("tags", [])

        self.hb = HashBuilder({"type": "aggregation", "tags": tags })


        self.retentions_raw = conf.get("retentions", ["10s:1w"])
        self.retentions = [self.parse_retentions(r) for r in self.retentions_raw]

        self.time_retentions = [time.time() for _ in self.retentions]
        self.values_retentions = [[] for _ in self.retentions]
        self.historic_retentions = [[None for _ in range(persist)] for delta, persist in self.retentions]

    def filter(self, message):
        if self.query.match(message):
            now = time.time()
            for i, t in enumerate(self.time_retentions):
                if t + self.retentions[i][0] < now:
                    while self.time_retentions[i] + self.retentions[i][0] < now:
                        self.time_retentions[i] += self.retentions[i][0]
                    self.hb.build()
                    r = self.hb.dict()
                    r["value"] = self.operation(self.values_retentions[i])
                    self.historic_retentions[i].pop(0)
                    self.historic_retentions[i].append(r["value"])
                    r["historic"] = self.historic_retentions[i]
                    r["retentions"] = self.retentions_raw[i]
                    r["values"] = self.values_retentions[i]
                    self.values_retentions[i] = []
                    yield r

            [l.append(self.key.navigate(message)) for l in self.values_retentions]

        yield message
