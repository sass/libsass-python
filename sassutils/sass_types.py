""":mod:`sassutils.sass_types` --- Provides datatypes for custom functions.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides datatypes to be used in custom sass functions.

The following mappings from sass types to python types are used:

SASS_NULL: ``None``
SASS_BOOLEAN: ``True`` or ``False``
SASS_STRING: class:`str`
SASS_NUMBER: class:`SassNumber`
SASS_COLOR: class:`SassColor`
SASS_LIST: class:`SassList`
SASS_MAP: class:`dict` or class:`SassMap`
SASS_ERROR: class:`SassError`
SASS_WARNING: class:`SassWarning`
"""
from __future__ import absolute_import
from __future__ import unicode_literals

from collections import namedtuple

from six import text_type


class SassNumber(namedtuple('SassNumber', ('value', 'unit'))):
    def __new__(cls, value, unit):
        value = float(value)
        if not isinstance(unit, text_type):
            unit = unit.decode('UTF-8')
        return super(SassNumber, cls).__new__(cls, value, unit)


class SassColor(namedtuple('SassColor', ('r', 'g', 'b', 'a'))):
    def __new__(cls, r, g, b, a):
        r = float(r)
        g = float(g)
        b = float(b)
        a = float(a)
        return super(SassColor, cls).__new__(cls, r, g, b, a)


SASS_SEPARATOR_COMMA = namedtuple('SASS_SEPARATOR_COMMA', ())()
SASS_SEPARATOR_SPACE = namedtuple('SASS_SEPARATOR_SPACE', ())()
SEPARATORS = frozenset((SASS_SEPARATOR_COMMA, SASS_SEPARATOR_SPACE))


class SassList(namedtuple('SassList', ('items', 'separator'))):
    def __new__(cls, items, separator):
        items = tuple(items)
        assert separator in SEPARATORS
        return super(SassList, cls).__new__(cls, items, separator)


class SassError(namedtuple('SassError', ('msg',))):
    def __new__(cls, msg):
        if not isinstance(msg, text_type):
            msg = msg.decode('UTF-8')
        return super(SassError, cls).__new__(cls, msg)


class SassWarning(namedtuple('SassError', ('msg',))):
    def __new__(cls, msg):
        if not isinstance(msg, text_type):
            msg = msg.decode('UTF-8')
        return super(SassWarning, cls).__new__(cls, msg)


class SassMap(dict):
    """Because sass maps can have mapping types as keys, we need an immutable
    hashable mapping type.
    """
    __slots__ = ('_hash',)

    def __new__(cls, *args, **kwargs):
        value = super(SassMap, cls).__new__(cls, *args, **kwargs)
        # An assertion that all things are hashable
        value._hash = hash(frozenset(value.items()))
        return value

    def __repr__(self):
        return '{0}({1})'.format(type(self).__name__, frozenset(self.items()))

    def __hash__(self):
        return self._hash

    def _immutable(self, *_):
        raise AssertionError('SassMaps are immutable')

    __setitem__ = __delitem__ = _immutable
