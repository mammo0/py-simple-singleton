"""
Simple singelton pattern for python.
thanks to wowkin2 (https://gist.github.com/wowkin2/3af15bfbf197a14a2b0b2488a1e8c787)
"""
import inspect
from typing import Dict, Callable, Union, Any, List, FrozenSet, Tuple, TypeVar, Generic


T = TypeVar("T", bound="_SingletonArgsMeta")


class _SingletonArgsMeta(type, Generic[T]):
    """
    Singleton that keep single instance for single set of arguments.
    """
    _instances: Dict[int, T] = {}
    _init: Dict[T, Callable] = {}

    def __init__(cls: T, name: str, bases: tuple, dct: dict) -> None:
        super(_SingletonArgsMeta, cls).__init__(name, bases, dct)

        # save the __init__ method of each class that uses this singleton
        # required in __call__ method below
        cls._init[cls] = getattr(cls, "__init__")

    def __call__(cls: T, *args, **kwargs) -> T:
        # get the individual calling signature of the __init__ method for this class
        init_callargs: Dict[str, Any] = inspect.getcallargs(cls._init[cls], None, *args, **kwargs)

        # create a key
        key: int = hash(
            # the individual key is this class combined with the signature above
            (cls, cls.__freeze(init_callargs))
        )

        # check if there's already an instance that has the same __init__ signature
        if key not in cls._instances:
            # if not, create it
            cls._instances[key] = super(_SingletonArgsMeta, cls).__call__(*args, **kwargs)

        return cls._instances[key]

    def __freeze(cls, set_obj: Union[Dict[Any, Any], List[Any], Tuple[Any]]) -> Union[FrozenSet[Any], Tuple[Any], Any]:
        """
        Recursively transform a dictionary to a frozenset. This can be hashed.
        @param set_obj: The dictionary that should be converted.
        @return: A frozenset from the above dictionary.
        """
        if isinstance(set_obj, dict):
            return frozenset((key, cls.__freeze(value)) for key, value in set_obj.items())
        elif isinstance(set_obj, list):
            return tuple(cls.__freeze(value) for value in set_obj)
        return set_obj
