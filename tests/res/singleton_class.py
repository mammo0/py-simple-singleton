from simple_singleton import Singleton, ThreadSingleton
from tests.res import TestSingletonBase


class TestSingleton(TestSingletonBase, metaclass=Singleton):
    pass


class TestThreadSingleton(TestSingletonBase, metaclass=ThreadSingleton):
    pass
