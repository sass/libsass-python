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


def build_directory(sass_path, css_path, _root_sass=None, _root_css=None):
    """Compiles all SASS/SCSS files in ``path`` to CSS.

    :param sass_path: the path of the directory which contains source files
                      to compile
    :type sass_path: :class:`basestring`
    :param css_path: the path of the directory compiled CSS files will go
    :type css_path: :class:`basestring`
    :returns: a dictionary of source filenames to compiled CSS filenames
    :rtype: :class:`collections.Mapping`

    """
    if _root_sass is None or _root_css is None:
        _root_sass = sass_path
        _root_css = css_path
    result = {}
    if not os.path.isdir(css_path):
        os.mkdir(css_path)
    for name in os.listdir(sass_path):
        if not SUFFIX_PATTERN.search(name):
            continue
        sass_fullname = os.path.join(sass_path, name)
        if os.path.isfile(sass_fullname):
            css_fullname = os.path.join(css_path, name) + '.css'
            css = compile(filename=sass_fullname, include_paths=[_root_sass])
            with open(css_fullname, 'w') as css_file:
                css_file.write(css)
            result[os.path.relpath(sass_fullname, _root_sass)] = \
                os.path.relpath(css_fullname, _root_css)
        elif os.path.isdir(sass_fullname):
            css_fullname = os.path.join(css_path, name)
            subresult = build_directory(sass_fullname, css_fullname,
                                        _root_sass, _root_css)
            result.update(subresult)
    return result
