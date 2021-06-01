from simple_singleton import Singleton, ThreadSingleton
from tests.res import TSingletonBase


class TSingleton(TSingletonBase, metaclass=Singleton):
    pass


class TThreadSingleton(TSingletonBase, metaclass=ThreadSingleton):
    pass
