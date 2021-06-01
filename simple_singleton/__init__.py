from simple_singleton.singleton import _SingletonMeta
from simple_singleton.singleton_args import _SingletonArgsMeta
from simple_singleton.thread_singleton import _ThreadSingletonMeta, \
    _ThreadSingletonArgsMeta


__all__ = ["Singleton", "ThreadSingleton", "SingletonArgs", "ThreadSingletonArgs"]


Singleton = _SingletonMeta
ThreadSingleton = _ThreadSingletonMeta
SingletonArgs = _SingletonArgsMeta
ThreadSingletonArgs = _ThreadSingletonArgsMeta
