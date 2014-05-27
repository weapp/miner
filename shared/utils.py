import re

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



