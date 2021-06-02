"""
Extension for the singleton pattern to make it thread safe.
thanks to TonyDiana for the idea (https://github.com/mammo0/py-simple-singleton/pull/5)
"""
from threading import Lock

from .singleton import _SingletonMeta
from .singleton_args import _SingletonArgsMeta


class _ThreadSafeMixin(type):
    def __init__(cls, name: str, bases: tuple, dct: dict):
        super(_ThreadSafeMixin, cls).__init__(name, bases, dct)

        # add a lock for thread safety
        cls._lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        # use the lock
        with cls._lock:
            return super(_ThreadSafeMixin, cls).__call__(*args, **kwargs)


class _ThreadSingletonMeta(_ThreadSafeMixin, _SingletonMeta):
    pass


class _ThreadSingletonArgsMeta(_ThreadSafeMixin, _SingletonArgsMeta):
    pass
