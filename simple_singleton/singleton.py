"""
Simple singelton pattern for python.
thanks to wowkin2 (https://gist.github.com/wowkin2/3af15bfbf197a14a2b0b2488a1e8c787)
"""


class _SingletonMeta(type):
    """
    Simple Singleton that keep only one value for all instances.
    """
    def __init__(cls, name: str, bases: tuple, dct: dict):
        super(_SingletonMeta, cls).__init__(name, bases, dct)

        # this variable holds the singleton instance
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        # check if there's already an instance
        if cls.instance is None:
            # if not create one
            cls.instance = super(_SingletonMeta, cls).__call__(*args, **kwargs)

        # return the instance
        return cls.instance
