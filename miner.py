#!/usr/bin/env python

import os
import argparse
from multiprocessing import Process

import yaml
import json

from shared.utils import build_components, build_component, apply_envs
from shared.path import Path

if __name__ == '__main__':

    # print "Visit this!"
    # print "http://wubytes.com/w/grid/example:cpu,swap,memory,procs,networkout,networkin"
    # print

    parser = argparse.ArgumentParser()
    parser.add_argument("--secrets", help="yml file for your secret data", default=None)
    parser.add_argument("--conf", help="publish the string you use here", default=None)
    parser.add_argument("--publish", help="publish the string you use here")
    parser.add_argument("--publisher", help="publish the string you use here", type=build_component)
    args = parser.parse_args()

    confpath = args.conf or os.path.join(os.path.dirname(os.path.realpath(__file__)), "conf.yml")
    conf = yaml.load(open(confpath))

    try:
        default_secret = os.path.join(os.path.dirname(os.path.realpath(__file__)), "secrets.yml")
        secretspath = args.secrets or default_secret
        secrets = yaml.load(open(secretspath)) or {}
    except IOError:
        if secretspath == default_secret:
            secrets = {}
        else:
            raise


    
    
    environ = dict(os.environ)
    environ.update(secrets)

    conf = apply_envs(conf, environ)

    if args.publisher:
        publishers=[args.publisher]
    else:
        publishers = build_components(conf, "publishers")

    if args.publish:
        [p(json.loads(args.publish)) for p in publishers]
    else:
        extractors = build_components(conf, "extractors")
        process = [Process(**extractor(publishers)) for extractor in extractors]
        [p.start() for p in process]
        [p.join() for p in process]
