from threading import Thread, Event, Semaphore
import threading
from typing import Union, Any, Tuple, Dict, Optional, Callable
import unittest

from simple_singleton import Singleton, SingletonArgs
from tests.res import TSingletonBase
from tests.res.singleton_args_class import TSingletonArgs, TThreadSingletonArgs
from tests.res.singleton_class import TThreadSingleton, TSingleton
from types import FrameType


CONSTRUCTOR_CALL_SEMAPHORE: Semaphore = Semaphore(0)
BREAKPOINT: Event = Event()


def custom_trace(frame: FrameType, event: str, _: Any) -> Callable[[FrameType, str, Any],
                                                                   Optional[Callable[..., Any]]]:
    # set a 'breakpoint' when leaving the constructor of the TSingletonBase class
    if (event == "return" and
            frame.f_code == getattr(TSingletonBase.__init__, "__code__")):
        CONSTRUCTOR_CALL_SEMAPHORE.release()
        # now wait
        BREAKPOINT.wait()

    # should return itself as mentioned in the documentation
    return custom_trace


class TestNormal(unittest.TestCase):
    __default_trace: Callable[[FrameType, str, Any], Optional[Callable[..., Any]]] = threading._trace_hook  # noqa

    @classmethod
    def setUpClass(cls) -> None:
        # apply the custom tracing function
        threading.settrace(custom_trace)

    @classmethod
    def tearDownClass(cls) -> None:
        # reset to the default tracing function
        threading.settrace(cls.__default_trace)

        # reset the singleton classes (for further tests)
        TSingleton._instance = None
        TSingletonArgs._instances.clear()  # noqa

    def setUp(self) -> None:
        # reset everything before each test run
        BREAKPOINT.clear()
        with CONSTRUCTOR_CALL_SEMAPHORE._cond:  # noqa
            CONSTRUCTOR_CALL_SEMAPHORE._value = 0  # noqa
            CONSTRUCTOR_CALL_SEMAPHORE._cond.notify()  # noqa

    def test_normal_singleton(self) -> None:
        # create two instances of a singleton
        w1: SingletonFactory = SingletonFactory(TSingleton)
        w2: SingletonFactory = SingletonFactory(TSingleton)
        w1.start()
        w2.start()

        # because there is no Lock in these classes, the constructor of the singleton class will be be run twice
        with CONSTRUCTOR_CALL_SEMAPHORE._cond:  # noqa
            CONSTRUCTOR_CALL_SEMAPHORE._cond.wait_for(lambda: CONSTRUCTOR_CALL_SEMAPHORE._value == 2)  # noqa
        # release the break; the threads should exit now
        BREAKPOINT.set()

        # wait for them to finish
        w1.join()
        w2.join()

        # the singleton constructor was called twice, so the instances can't be equal
        # this means the Singleton is not thread safe
        self.assertNotEqual(w1.singleton, w2.singleton)

    def test_nomal_singletonargs(self) -> None:
        # create two instances of a singleton with same arguments
        w1: SingletonFactory = SingletonFactory(TSingletonArgs, "instance1")
        w2: SingletonFactory = SingletonFactory(TSingletonArgs, "instance1")
        w1.start()
        w2.start()

        # because there is no Lock in these classes, the constructor of the singleton class will be be run twice
        with CONSTRUCTOR_CALL_SEMAPHORE._cond:  # noqa
            CONSTRUCTOR_CALL_SEMAPHORE._cond.wait_for(lambda: CONSTRUCTOR_CALL_SEMAPHORE._value == 2)  # noqa
        # release the break; the threads should exit now
        BREAKPOINT.set()

        # wait for them to finish
        w1.join()
        w2.join()

        # the singleton constructor was called twice, so the instances can't be equal
        # this means the SingletonArgs is not thread safe
        self.assertNotEqual(w1.singleton, w2.singleton)


class TestThread(unittest.TestCase):
    __default_trace: Callable[[FrameType, str, Any], Optional[Callable[..., Any]]] = threading._trace_hook  # noqa

    @classmethod
    def setUpClass(cls) -> None:
        # apply the custom tracing function
        threading.settrace(custom_trace)

    @classmethod
    def tearDownClass(cls) -> None:
        # reset to the default tracing function
        threading.settrace(cls.__default_trace)

        # reset the singleton classes (for further tests)
        TThreadSingleton._instance = None
        TThreadSingletonArgs._instances.clear()  # noqa

    def setUp(self) -> None:
        # reset everything before each test run
        BREAKPOINT.clear()
        with CONSTRUCTOR_CALL_SEMAPHORE._cond:  # noqa
            CONSTRUCTOR_CALL_SEMAPHORE._value = 0  # noqa
            CONSTRUCTOR_CALL_SEMAPHORE._cond.notify()  # noqa

    def test_thread_singleton(self) -> None:
        # create two instances of a singleton
        w1: SingletonFactory = SingletonFactory(TThreadSingleton)
        w2: SingletonFactory = SingletonFactory(TThreadSingleton)
        w1.start()
        w2.start()

        # because of the Lock in these classes, the constructor of the singleton can be called only once at this time
        with CONSTRUCTOR_CALL_SEMAPHORE._cond:  # noqa
            CONSTRUCTOR_CALL_SEMAPHORE._cond.wait_for(lambda: CONSTRUCTOR_CALL_SEMAPHORE._value == 1)  # noqa
        # release the break; the threads should exit now
        BREAKPOINT.set()

        # wait for them to finish
        w1.join()
        w2.join()

        # ensure that the singleton constructor was only called once
        self.assertEqual(CONSTRUCTOR_CALL_SEMAPHORE._value, 1)  # noqa

        # check the equality of the instances
        # this means the ThreadSingleton is thread safe
        self.assertEqual(w1.singleton, w2.singleton)

    def test_thread_singletonargs(self) -> None:
        # create two instances of a singleton with same arguments and one with a different argument
        w1: SingletonFactory = SingletonFactory(TThreadSingletonArgs, "instance1")
        w2: SingletonFactory = SingletonFactory(TThreadSingletonArgs, "instance1")
        w3: SingletonFactory = SingletonFactory(TThreadSingletonArgs, "instance2")
        w1.start()
        w2.start()
        w3.start()

        # because of the Lock in these classes, the constructor of the singleton can be called only once at this time
        with CONSTRUCTOR_CALL_SEMAPHORE._cond:  # noqa
            CONSTRUCTOR_CALL_SEMAPHORE._cond.wait_for(lambda: CONSTRUCTOR_CALL_SEMAPHORE._value == 1)  # noqa
        # release the break; the threads should exit now
        BREAKPOINT.set()

        # wait for them to finish
        w1.join()
        w2.join()
        w3.join()

        # ensure that the singleton constructor was only called twice
        # twice, because one singleton was initialized with a different argument
        self.assertEqual(CONSTRUCTOR_CALL_SEMAPHORE._value, 2)  # noqa

        # check the equality of the first two instances
        # this means the ThreadSingletonArgs is thread safe
        self.assertEqual(w1.singleton, w2.singleton)

        # however, the first and third instances must not be equal
        self.assertNotEqual(w1.singleton, w3.singleton)


# helper class that wraps the creation of a singleton instance into a thread
class SingletonFactory(Thread):
    def __init__(self, singleton_cls: Union[Singleton, SingletonArgs], *args, **kwargs) -> None:
        Thread.__init__(self, group=None, target=None, name=None, args=(), kwargs=None, daemon=None)

        self.singleton: Union[Singleton, SingletonArgs, None] = None
        self.__singleton_cls: Union[Singleton, SingletonArgs] = singleton_cls
        self.__args: Tuple[Any, ...] = args
        self.__kwargs: Dict[str, Any] = kwargs

    def run(self) -> None:
        self.singleton = self.__singleton_cls(*self.__args, **self.__kwargs)


if __name__ == "__main__":
    unittest.main()
