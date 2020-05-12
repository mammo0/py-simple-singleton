from simple_singleton.singleton import _SingletonMeta
from simple_singleton.singleton_args import _SingletonArgsMeta


__all__ = ["Singleton", "SingletonArgs"]


Singleton = _SingletonMeta
SingletonArgs = _SingletonArgsMeta
