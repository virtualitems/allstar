# coding:utf-8

# Author:
#   Alejandro CR
#   contacto@alejandrocr.co
#   https://github.com/virtualitems/

# Project:
#   allstar
#   https://github.com/virtualitems/allstar
#   https://pypi.org/project/allstar/

# License:
#   MIT License
#
#   Copyright (c) 2022 Virtual Items
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all
#   copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.

"""
Testing the star module
"""

import unittest
import logging

from builtins import *  # testing

from allstar import Star

logging.basicConfig(level=logging.DEBUG)
logging.captureWarnings(True)

__all__ = []


def module_scope_sign():
    """testing"""


def module_scope_include_string():
    """testing"""


def module_scope_include_reference():
    """testing"""


class StarTest(unittest.TestCase):
    """Test the Star class"""

    def test_instance(self):
        """The instance must be the Star object exports reference"""
        star = Star(__name__)
        self.assertIs(star._exports, __all__)

    def test_sign(self):
        """The sign decorator must add the callable to the exports list"""
        star = Star(__name__)
        star.sign(module_scope_sign)
        self.assertIn('module_scope_sign', __all__)

    def test_sign_exception(self):
        """The sign decorator must raise an error if the item is not in the module scope"""
        star = Star(__name__)
        def local_scope_method(): ...
        self.assertRaises(AttributeError, star.sign, local_scope_method)

    def test_include_reference(self):
        """The include method must add the callable to the exports list using a reference"""
        star = Star(__name__)
        star.include(module_scope_include_reference)
        self.assertIn('module_scope_include_reference', __all__)

    def test_include_string(self):
        """The include method must add the callable to the exports list using a string"""
        star = Star(__name__)
        star.include('module_scope_include_string')
        self.assertIn('module_scope_include_string', __all__)

    def test_include_module_reference(self):
        """The include method must add the callable to the exports list using a module"""
        star = Star(__name__)
        star.include(str)
        self.assertIn('str', __all__)

    def test_include_module_string(self):
        """The include method must add the callable to the exports list using a module"""
        star = Star(__name__)
        star.include('int')
        self.assertIn('int', __all__)

    def test_include_reference_exception(self):
        """The include method must raise an error if the item is not in the module scope"""
        star = Star(__name__)
        def local_scope_method(): ...
        self.assertRaises(AttributeError, star.include, local_scope_method)

    def test_include_string_exception(self):
        """The include method must raise an error if the item is not in the module scope"""
        star = Star(__name__)
        self.assertRaises(AttributeError, star.include, 'local_scope_method')

    def test_include_all(self):
        """The include_all method must add the callables to the exports list"""
        star = Star(__name__)
        star.include_all(['list'])
        self.assertIn('list', __all__)

    def test_commit(self):
        """The commit method must merge the names added manually"""
        star = Star(__name__)
        __all__ = ['tuple']
        star.commit()
        self.assertIn('tuple', __all__)


if __name__ == '__main__':
    unittest.main()
