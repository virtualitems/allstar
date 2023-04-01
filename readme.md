# AllStar

Allstar is a simple library for modules \_\_all\_\_ iterable management.

The \_\_all\_\_ iterable is used to define what is imported when you use `from module import *`. This kind of import is used by project mappers like documentation generators. It is important because, for example, you don't want to generate the documentation for the defined classes and all the imported ones.

> it is called "allstar" because \_\_all\_\_ is imported using an star ( * ) symbol

# Usage

## Basic usage

```python
from allstar import Star

# manager instance
# __name__ is used to reference the module and its attributes
star = Star(__name__)

# star.sign adds a callable to the __all__ iterable
@star.sign
class TheClass:
    pass

@star.sign
def the_function():
    pass

print(__all__)  # prints: ['TheClass', 'the_function']
```

## Extended usage

```python
import os, sys, builtins

from allstar import Star

__all__ = ['os']  # Star preserves the previous names

star = Star(__name__)

star.include('builtins')  # include names using strings or references

star.include_all(['os', 'sys'])  # include names using iterables
```

## Some extra features

```python
from allstar import Star

star = Star(__name__)

star.empty()  # empties the __all__ iterable

star.freeze()  # turns the __all__ iterable into a tuple
```