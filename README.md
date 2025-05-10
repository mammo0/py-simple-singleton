# Simple Python Singleton pattern

![PyPI package](https://github.com/mammo0/py-simple-singleton/workflows/PyPI%20package/badge.svg)
[![PyPI version](https://badge.fury.io/py/simple-singleton.svg)](https://badge.fury.io/py/simple-singleton)

This module provides a simple way to define a class as a singleton.


### Install

You can install this python module via **pip**:
```shell
pip install simple-singleton
```

Otherwise the module can be downloaded from PyPI: https://pypi.org/project/simple-singleton/


### Usage

1. Import the module:
   ```python
   from simple_singleton import Singleton
   ```
   or:
   ```python
   from simple_singleton import SingletonArgs
   ```
2. Create a class that uses one of the above meta classes:
   ```python
   class NewClass(metaclass=Singleton):
       pass
   ```
   or:
   ```python
   class NewClass(metaclass=SingletonArgs):
       pass
   ```


### Difference between `Singleton` and `SingletonArgs`

The `Singleton` class is a very basic implementation of the singleton pattern. All instances of a class are equal. Even if they are initialized with different parameters:
```python
instance1 = SingletonClass(param="value")
instance2 = SingletonClass(param="different_value")

assert instance1 == instance2  # True
print(instance2.param)         # "value"
```

**If you do not want this behavior**, use the `SingletonArgs` meta class. With this class only instances that are initialized with the same parameters are the equal:
```python
instance1 = SingletonArgsClass(param="value")
instance2 = SingletonArgsClass(param="different_value")
instance3 = SingletonArgsClass(param="value")

assert instance1 == instance2  # False
assert instance1 == instance3  # True

print(instance2.param)         # "different_value"
```


### Usage in multi-threaded environments

**The `Singleton` and `SingletonArgs` meta classes are not thread-safe!**

To use them in a multi-threaded environment, please use the

- `ThreadSingleton` and
- `ThreadSingletonArgs`

meta classes. They can be used exactly like the standard meta classes.
