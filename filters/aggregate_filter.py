#!/usr/bin/env python
from base_filter import BaseFilter
from shared.hash_builder import HashBuilder
from shared.query import Query
from shared.path import Path
from shared.utils import parse_retentions

import time

import re

import numpy as np

re_d = re.compile("^\s*(\d+(?:.\d+)?)")

class Operation:
    def __init__(self, operation):
        self.operation_name = operation
        self.operation = {
            "count": self.len,
            "avg": self.avg,
            "median": self.median,
            "percentile_95": self.avg,
            "max": self.max,
            "min": self.min,
        }[operation]

    def __call__(self, values):
        self.store_values(values)
        return self.operation()

    def len(self):
        return len(self.__values)

    def median(self):
        return np.percentile(self.__float_values, 50)

    def percentile_95(self):
        return np.percentile(self.__float_values, 95)

    def max(self):
        if self.__float_values:
            return max(self.__float_values)

    def min(self):
        if self.__float_values:
            return min(self.__float_values)

    def avg(self):
        if self.__float_values:
            return sum(self.__float_values)/len(self.__float_values)

    def store_values(self, values):
        self.__values = values
        self.__float_values = self.float_values(values)

    def float_values(self, values):
        return [float(re_d.match(v).group(1) or 0) for v in values if v is not None]

class AggregateFilter(BaseFilter):


    def __init__(self, conf):
        BaseFilter.__init__(self, conf)
        self.query = Query(self.conf.get("query"))
        self.key = Path(self.conf.get("key", "/"))
        self.raw_operations = sorted(set(self.conf.get("operations", ["count"])))
        self.operations = [Operation(op) for op in self.raw_operations]
        self.raw_retentions = conf.get("retentions", ["10s:1w"])
        self.retentions = [parse_retentions(r) for r in self.raw_retentions]

        tags = ["generated", "aggregate"] + self.raw_operations + self.conf.get("tags", [])
        self.hb = HashBuilder({"type": "aggregation", "tags": tags })
        self.time_retentions = [time.time() for _ in self.retentions]
        self.values_retentions = [[] for _ in self.retentions]
        self.historic_retentions = [{op: [None for _ in range(persist)] for op in self.raw_operations} for delta, persist in self.retentions]

    def filter(self, message):
        if self.query.match(message):
            now = time.time()
            for i, t in enumerate(self.time_retentions):
                if t + self.retentions[i][0] < now:
                    while self.time_retentions[i] + self.retentions[i][0] < now:
                        self.time_retentions[i] += self.retentions[i][0]
                    self.hb.build()
                    r = self.hb.dict()
                    values = [op(self.values_retentions[i]) for op in self.operations]
                    r["fields"] = dict(zip(self.raw_operations, values))
                    [self.historic_retentions[i][op].pop(0) for op in self.raw_operations]
                    [self.historic_retentions[i][op].append(r["fields"][op]) for op in self.raw_operations]
                    r["historic"] = self.historic_retentions[i]
                    r["retentions"] = self.raw_retentions[i]
                    r["values"] = self.values_retentions[i]
                    self.values_retentions[i] = []
                    yield r

            [l.append(self.key.navigate(message)) for l in self.values_retentions]

        yield message
