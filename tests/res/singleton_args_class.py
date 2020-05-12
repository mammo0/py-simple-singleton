from tests.res import TestSingletonBase
from simple_singleton import SingletonArgs


class TestSingletonArgs(TestSingletonBase, metaclass=SingletonArgs):
    pass


class TestSingletonArgsWithoutInit(metaclass=SingletonArgs):
    # no __init__ method in this class
    pass
