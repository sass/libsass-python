""":mod:`sassutils.utils` --- Utilities for internal use
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import collections
import functools
import os.path


__all__ = 'is_mapping', 'relpath'


def is_mapping(value):
    """The predicate method equivalent to::

        isinstance(value, collections.Mapping)

    This function works on Python 2.5 as well.

    :param value: a value to test its type
    :returns: ``True`` only if ``value`` is a mapping object
    :rtype: :class:`bool`

    """
    return isinstance(value, collections.Mapping)


if not hasattr(collections, 'Mapping'):
    @functools.wraps(is_mapping)
    def is_mapping(value):
        return (callable(getattr(value, 'keys', None)) and
                callable(getattr(value, 'values', None)) and
                callable(getattr(value, 'items', None)) and
                callable(getattr(value, '__getitem__', None)))


def relpath(path, start=os.path.curdir):
    """Equivalent to :func:`os.path.relpath()` except it's for
    Python 2.5.

    """
    start_list = os.path.abspath(start).split(os.path.sep)
    path_list = os.path.abspath(path).split(os.path.sep)
    # Work out how much of the filepath is shared by start and path.
    i = len(os.path.commonprefix([start_list, path_list]))
    rel_list = [os.path.pardir] * (len(start_list)-i) + path_list[i:]
    if not rel_list:
        return os.path.curdir
    return os.path.join(*rel_list)


if hasattr(os.path, 'relpath'):
    relpath = os.path.relpath
