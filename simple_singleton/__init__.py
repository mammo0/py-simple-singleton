from .singleton import _SingletonMeta
from .singleton_args import _SingletonArgsMeta


__all__ = ["Singleton", "SingletonArgs"]


Singleton = _SingletonMeta
SingletonArgs = _SingletonArgsMeta
