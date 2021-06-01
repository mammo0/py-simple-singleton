from simple_singleton import SingletonArgs, ThreadSingletonArgs
from tests.res import TestSingletonBase


class TestSingletonArgs(TestSingletonBase, metaclass=SingletonArgs):
    pass


class TestSingletonArgsWithoutInit(metaclass=SingletonArgs):
    # no __init__ method in this class
    pass


class TestThreadSingletonArgs(TestSingletonBase, metaclass=ThreadSingletonArgs):
    pass
