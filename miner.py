import yaml
from multiprocessing import Process
from lib.utils import build_components

if __name__ == '__main__':
    conf = yaml.load(open("conf.yml"))
    publishers = build_components(conf, "publishers")
    extractors = build_components(conf, "extractors")
    process = [Process(**extractor(publishers)) for extractor in extractors]
    [p.start() for p in process]
    [p.join() for p in process]
