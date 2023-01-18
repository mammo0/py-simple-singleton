from .singleton import _SingletonMeta
from .singleton_args import _SingletonArgsMeta
from .thread_singleton import _ThreadSafeMixin


__all__ = ["Singleton", "ThreadSingleton", "SingletonArgs", "ThreadSingletonArgs"]


class Singleton(_SingletonMeta):
    pass


class ThreadSingleton(_ThreadSafeMixin, Singleton):
    pass


class SingletonArgs(_SingletonArgsMeta):
    pass


class ThreadSingletonArgs(_ThreadSafeMixin, SingletonArgs):
    pass
