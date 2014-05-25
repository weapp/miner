import argparse
from multiprocessing import Process

import yaml
import json

from shared.utils import build_components, build_component

if __name__ == '__main__':

    print "Visit this!"
    print "http://wubytes.com/w/grid/example:cpu,swap,memory,procs,networkout,networkin"
    print

    parser = argparse.ArgumentParser()
    parser.add_argument("--conf", help="publish the string you use here", default="conf.yml")
    parser.add_argument("--publish", help="publish the string you use here")
    parser.add_argument("--publisher", help="publish the string you use here", type=build_component)
    args = parser.parse_args()

    conf = yaml.load(open(args.conf))

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
