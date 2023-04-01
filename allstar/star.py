# coding:utf-8

"""
Dynamically add names to the module's __all__ list
"""

# ------------------------------
# IMPORT MODULES
# ------------------------------

# standard library
from sys import modules

# typing
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Callable, Iterable, Union


# ------------------------------
# __all__
# ------------------------------

__all__ = ('Star',)


# ------------------------------
# DOMAIN
# ------------------------------

def is_iterable(obj: 'Any') -> 'bool':
    """verify if an object is iterable

    Examples:

        >>> is_iterable('string')
        True

        >>> is_iterable(1)
        False

    Args:
        obj: Object to verify

    Returns:
        True if obj is iterable, False otherwise

    """
    try:
        return callable(obj.__iter__)
    except AttributeError:
        return False


class Star:
    """__all__ list manager

    Examples:

        >>> from allstar import Stard

    Attributes:
        _exports: Current __all__ names list
        _module: Module reference
        _frozen_reference: Reference to the freeze function generated tuple
    """

    def __init__(self, module_name: 'str'):
        """
        Args:
            module_name: Name of the module to manage

        Raises:
            AssertionError: if the arguments are not of the correct type
            ModuleNotFoundError: if the module is not found in sys.modules
        """
        assert isinstance(module_name, str), 'module_name must be a string'

        # set defaults
        self._exports = []
        self._frozen_reference = None

        self._module = modules.get(module_name)

        if not self._module:
            raise ModuleNotFoundError(f'{module_name} module not found')

        # merge current names and set the list reference
        if hasattr(self._module, '__all__') and \
           is_iterable(self._module.__all__):

            names = self._clean_names_iterable(self._module.__all__)
            self._exports.extend(names)

        # use the manager reference
        self._module.__all__ = self._exports

    def __contains__(self, item):
        if not isinstance(item, str):
            return False

        return item in self._exports

    def __iter__(self):
        return iter(self._exports)

    def __len__(self):
        return len(self._exports)

    def __repr__(self):
        return repr(self._exports)

    def __str__(self):
        return str(self._exports)

    def _store(self, name: 'str'):
        """Save a module's member name to the __all__ list

        Args:
            name: Name of the member to add to the __all__ list

        """
        assert isinstance(name, str), 'name must be a string'

        if name not in self._exports:
            self._exports.append(name)

    def _clean_name(self, item: 'Any') -> 'str':
        """Validate and clean the name of an item

        Args:
            item: Item to validate and clean

        Returns:
            The name of the item

        Raises:
            TypeError: if the item is not a string or an object with a
                __name__ attribute

            AttributeError: if the item is not an attribute of the module
        """

        if isinstance(item, str):
            name = item

        elif hasattr(item, '__name__'):
            name = item.__name__

        else:
            raise TypeError(
                'item must be a string or an object with a __name__ attribute')

        if not hasattr(self._module, name):
            raise AttributeError(
                f'{item} is not an attribute of {self._module.__name__}')

        return name

    def _clean_names_iterable(self, iterable: 'Iterable') -> 'set':
        """Merge a list of names to the __all__ list

        Args:
            iterable: Iterable of names to merge

        Raises:
            AssertionError: if the argument is not an Iterable
        """
        assert is_iterable(iterable), 'iterable must be an Iterable'

        names_set = set()

        for item in iterable:
            names_set.add(self._clean_name(item))

        return names_set

    def _check_reference(self):
        """Check if the __all__ reference is the manager's reference.
        If not, merge the data and set the manager's reference.
        """
        if self._module.__all__ is self._frozen_reference:
            # the data is already in _exports
            self._module.__all__ = self._exports

        elif self._module.__all__ is not self._exports:
            # try to merge the found data
            self._merge(self._module.__all__)
            self._module.__all__ = self._exports

    def _merge(self, iterable: 'Iterable'):
        """Merge a list of names to the __all__ list

        Args:
            iterable: Iterable of names to merge
        """
        names = self._clean_names_iterable(iterable)

        for name in names:
            self._store(name)

    def sign(self, item: 'Callable'):
        """Decorator to add an object to the __all__ list

        Examples:

            # with a class

            >>> star = Star()
            >>> @star.sign
            ... class Example:
            ...     pass
            >>> __all__
            ['Example']

            # With a function

            >>> star = Star()
            >>> @star.sign
            ... def example():
            ...     pass
            >>> __all__
            ['example']

        Args:
            item: Object to add to the exports list

        Returns:
            The same object passed as argument

        Raises:
            TypeError: if item is not callable
            AttributeError: if item has no __name__ attribute
        """

        if not callable(item):
            raise TypeError('item must be callable')

        if not hasattr(self._module, item.__name__):
            raise AttributeError(
                f'{item} is not an attribute of {self._module.__name__}')

        self._store(item.__name__)

        self._check_reference()

        return item

    def include(self, item: 'Union[str, Callable]'):
        """Add an object to the __all__ list

        Examples:

            >>> star = Star()
            >>> star.include('Example1')  # Example1 is a string
            >>> star.include(example2)  # example2 is a reference
            >>> __all__
            ['Example1', 'example2']

        Args:
            item: Object to add to the exports list
        """
        self._store(self._clean_name(item))

        self._check_reference()

    def include_all(self, iterable: 'Iterable'):
        """Merge the names contained in an iterable to the __all__ list

        Examples:

            >>> star = Star()
            >>> star.include_all(['Example1', 'example2'])
            >>> __all__
            ['Example1', 'example2']

        Args:
            iterable: Iterable of names to merge

        Raises:
            TypeError: if the argument is not an Iterable
        """
        if not is_iterable(iterable):
            raise TypeError(
                f'iterable must be an Iterable, not {type(iterable)}')

        self._merge(iterable)

        self._check_reference()

    def freeze(self):
        """Transform the __all__ list into a tuple

        Examples:

            >>> exports = Exports()
            >>> exports.freeze()
            >>> __all__
            ()
        """
        self._frozen_reference = tuple(self._exports)
        self._module.__all__ = self._frozen_reference

    def empty(self):
        """Create an empty exports list

        Examples:

            >>> exports = Exports()
            >>> exports.empty()
            >>> __all__
            []
        """
        self._exports.clear()
        self._module.__all__ = self._exports
