"""
Simple singelton pattern for python.
thanks to wowkin2 (https://gist.github.com/wowkin2/3af15bfbf197a14a2b0b2488a1e8c787)
"""
from typing import Optional, TypeVar, Generic, cast


T = TypeVar("T", bound="_SingletonMeta")


class _SingletonMeta(type, Generic[T]):
    """
    Simple Singleton that keep only one value for all instances.
    """
    _instance: Optional[T] = None

    def __call__(cls: T, *args, **kwargs) -> T:
        # check if there's already an instance
        if cls._instance is None:
            # if not create one
            cls._instance = cast(T, super().__call__(*args, **kwargs))

        # return the instance
        return cls._instance
