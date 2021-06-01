from simple_singleton import SingletonArgs, ThreadSingletonArgs
from tests.res import TSingletonBase


class TSingletonArgs(TSingletonBase, metaclass=SingletonArgs):
    pass


class TSingletonArgsWithoutInit(metaclass=SingletonArgs):
    # no __init__ method in this class
    pass


class TThreadSingletonArgs(TSingletonBase, metaclass=ThreadSingletonArgs):
    pass
