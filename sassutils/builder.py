""":mod:`sassutils.builder` --- Build the whole directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import os
import os.path
import re

from sass import compile

__all__ = 'SUFFIXES', 'SUFFIX_PATTERN', 'build_directory'


#: (:class:`collections.Set`) The set of supported filename suffixes.
SUFFIXES = frozenset(['sass', 'scss'])

#: (:class:`re.RegexObject`) The regular expression pattern which matches to
#: filenames of supported :const:`SUFFIXES`.
SUFFIX_PATTERN = re.compile('[.](' + '|'.join(map(re.escape, SUFFIXES)) + ')$')


def build_directory(path, root_path=None):
    """Compiles all SASS/SCSS files in ``path`` to CSS.

    :param path: the path of the directory which contains source files
                 to compile
    :type path: :class:`basestring`
    :returns: a dictionary of source filenames to compiled CSS filenames
    :rtype: :class:`collections.Mapping`

    """
    if root_path is None:
        root_path = path
    result = {}
    for name in os.listdir(path):
        if not SUFFIX_PATTERN.search(name):
            continue
        fullname = os.path.join(path, name)
        if os.path.isfile(fullname):
            css_name = fullname + '.css'
            css = compile(filename=fullname, include_paths=[root_path])
            with open(css_name, 'w') as css_file:
                css_file.write(css)
            result[os.path.relpath(fullname, root_path)] = \
                os.path.relpath(css_name, root_path)
        elif os.path.isdir(fullname):
            subresult = build_directory(fullname, root_path)
            result.update(subresult)
    return result
