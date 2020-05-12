from simple_singleton import Singleton
from tests.res import TestSingletonBase


class TestSingleton(TestSingletonBase, metaclass=Singleton):
    pass
