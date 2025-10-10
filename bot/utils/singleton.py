# -*- coding: utf-8 -*-


class Singleton(type):
    _instances = {}
    _class_ids = {}

    def __call__(cls, *args, **kwargs):
        key = f"{cls.__module__}.{cls.__name__}"
        mro_ids = tuple(id(base) for base in cls.__mro__ if base is not object)
        last_ids = Singleton._class_ids.get(key)
        if last_ids != mro_ids and key in Singleton._instances:
            del Singleton._instances[key]
        if key not in Singleton._instances:
            Singleton._instances[key] = super().__call__(*args, **kwargs)
            Singleton._class_ids[key] = mro_ids
        return Singleton._instances[key]

    @classmethod
    def clear(cls) -> None:
        cls._instances.clear()
        cls._class_ids.clear()
