# AllStar

"Allstar" is a simple library for managing the the \_\_all\_\_ attribute in modules.

The \_\_all\_\_ attribute is used to specify what is imported when using the `from module import *` syntax. This type of import is commonly used by project mapping tools like documentation generators. It is important to manage \_\_all\_\_ because, for example, you may not want to generate documentation for imported classes, only for the ones you have created.

> The library is named "allstar" because the \_\_all\_\_ attribute is imported using the star (*) symbol.

# Installation

```bash
pip install allstar
```

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


# Author

Alejandro CR

contacto@alejandrocr.co

https://github.com/virtualitems/


# Project

https://pypi.org/project/allstar/

https://github.com/virtualitems/allstar


# License

MIT License

Copyright (c) 2022 Virtual Items

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
