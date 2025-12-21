import hashlib
import importlib
import os
import sys


class Singleton(type):
    _instances = {}  # NOQA: RUF012
    _module_hashes = {}  # NOQA: RUF012

    @staticmethod
    def _get_file_hash(module_file):
        try:
            with open(module_file, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except OSError:
            return None

    def __call__(cls, *args, **kwargs):
        module_name = cls.__module__
        module = sys.modules.get(module_name)

        module_file = getattr(module, "__file__", None)
        if module_file and module_file.endswith(".pyc"):
            module_file = module_file[:-1]

        if module_file and os.path.exists(module_file):
            current_hash = cls._get_file_hash(module_file)
            last_hash = Singleton._module_hashes.get(module_name)

            if last_hash and current_hash and current_hash != last_hash:
                new_module = importlib.reload(module)
                Singleton._module_hashes[module_name] = current_hash
                key = f"{cls.__module__}.{cls.__name__}"
                if key in Singleton._instances:
                    del Singleton._instances[key]
                new_cls = getattr(new_module, cls.__name__)
                return new_cls(*args, **kwargs)
            if current_hash and not last_hash:
                Singleton._module_hashes[module_name] = current_hash
        key = f"{cls.__module__}.{cls.__name__}"
        if key not in Singleton._instances:
            Singleton._instances[key] = super().__call__(*args, **kwargs)

        return Singleton._instances[key]

    @classmethod
    def clear(cls) -> None:
        cls._instances.clear()
        cls._module_hashes.clear()
