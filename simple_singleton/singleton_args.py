"""
Simple singelton pattern for python.
thanks to wowkin2 (https://gist.github.com/wowkin2/3af15bfbf197a14a2b0b2488a1e8c787)
"""


import inspect


class _SingletonArgsMeta(type):
    """
    Singleton that keep single instance for single set of arguments.
    """
    _instances = {}
    _init = {}

    def __init__(cls, name: str, bases: tuple, dct: dict):
        super(_SingletonArgsMeta, cls).__init__(name, bases, dct)

        # save the __init__ method of each class that uses this singleton
        # required in __call__ method below
        cls._init[cls] = getattr(cls, "__init__")

    def __call__(cls, *args, **kwargs):
        # get the individual calling signature of the __init__ method for this class
        init_callargs = inspect.getcallargs(cls._init[cls], None, *args, **kwargs)

        # create a key
        key = hash(
            # the individual key is this class combined with the signature above
            (cls, cls.__freeze_dict(init_callargs))
        )

        # check if there's already an instance that has the same __init__ signature
        if key not in cls._instances:
            # if not, create it
            cls._instances[key] = super(_SingletonArgsMeta, cls).__call__(*args, **kwargs)

        return cls._instances[key]

    def __freeze_dict(cls, dct: dict) -> frozenset:
        """
        Recursively transform a dictionary to a frozenset. This can be hashed.
        @param dct: The dictionary that should be converted.
        @return: A frozenset from the above dictionary.
        """
        if isinstance(dct, dict):
            return frozenset((key, cls.__freeze_dict(value)) for key, value in dct.items())
        elif isinstance(dct, list):
            return tuple(cls.__freeze_dict(value) for value in dct)
        return dct
