import importlib
import pkgutil
import sys
from importlib import util


def reload_and_get(module_name: str, element: str):
    spec = importlib.util.find_spec(module_name)
    if spec and spec.submodule_search_locations:
        prefix = f"{module_name}."
        for finder, name, is_pkg in pkgutil.walk_packages(spec.submodule_search_locations, prefix):
            sys.modules.pop(name, None)
    sys.modules.pop(module_name, None)

    importlib.invalidate_caches()
    module = importlib.import_module(module_name)
    return getattr(module, element)
