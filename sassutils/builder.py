""":mod:`sassutils.builder` --- Build the whole directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from __future__ import with_statement

import os
import os.path
import re

from sass import compile
from .utils import is_mapping, relpath

__all__ = 'SUFFIXES', 'SUFFIX_PATTERN', 'Manifest', 'build_directory'


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
            result[relpath(sass_fullname, _root_sass)] = \
                relpath(css_fullname, _root_css)
        elif os.path.isdir(sass_fullname):
            css_fullname = os.path.join(css_path, name)
            subresult = build_directory(sass_fullname, css_fullname,
                                        _root_sass, _root_css)
            result.update(subresult)
    return result


class Manifest(object):
    """Building manifest of SASS/SCSS.

    :param sass_path: the path of the directory that contains SASS/SCSS
                      source files
    :type sass_path: :class:`basestring`
    :param css_path: the path of the directory to store compiled CSS
                     files
    :type css_path: :class:`basestring`

    """

    @classmethod
    def normalize_manifests(cls, manifests):
        if manifests is None:
            manifests = {}
        elif is_mapping(manifests):
            manifests = dict(manifests)
        else:
            raise TypeError('manifests must be a mapping object, not ' +
                            repr(manifests))
        for package_name, manifest in manifests.items():
            if not isinstance(package_name, basestring):
                raise TypeError('manifest keys must be a string of package '
                                'name, not ' + repr(package_name))
            if isinstance(manifest, Manifest):
                continue
            elif isinstance(manifest, tuple):
                manifest = Manifest(*manifest)
            elif isinstance(manifest, basestring):
                manifest = Manifest(manifest)
            else:
                raise TypeError(
                    'manifest values must be a sassutils.builder.Manifest, '
                    'a pair of (sass_path, css_path), or a string of '
                    'sass_path, not ' + repr(manifest)
                )
            manifests[package_name] = manifest
        return manifests

    def __init__(self, sass_path, css_path=None, wsgi_path=None):
        if not isinstance(sass_path, basestring):
            raise TypeError('sass_path must be a string, not ' +
                            repr(sass_path))
        if css_path is None:
            css_path = sass_path
        elif not isinstance(css_path, basestring):
            raise TypeError('css_path must be a string, not ' +
                            repr(css_path))
        if wsgi_path is None:
            wsgi_path = css_path
        elif not isinstance(wsgi_path, basestring):
            raise TypeError('wsgi_path must be a string, not ' +
                            repr(wsgi_path))
        self.sass_path = sass_path
        self.css_path = css_path
        self.wsgi_path = wsgi_path

    def resolve_filename(self, package_dir, filename):
        """Gets a proper full relative path of SASS source and
        CSS source that will be generated, according to ``package_dir``
        and ``filename``.

        :param package_dir: the path of package directory
        :type package_dir: :class:`basestring`
        :param filename: the filename of SASS/SCSS source to compile
        :type filename: :class:`basestring`
        :returns: a pair of (sass, css) path
        :rtype: :class:`tuple`

        """
        sass_path = os.path.join(package_dir, self.sass_path, filename)
        css_filename = filename + '.css'
        css_path = os.path.join(package_dir, self.css_path, css_filename)
        return sass_path, css_path

    def build(self, package_dir):
        """Builds the SASS/SCSS files in the specified :attr:`sass_path`.
        It finds :attr:`sass_path` and locates :attr:`css_path`
        as relative to the given ``package_dir``.

        :param package_dir: the path of package directory
        :type package_dir: :class:`basestring`
        :returns: the set of compiled CSS filenames
        :rtype: :class:`collections.Set`

        """
        sass_path = os.path.join(package_dir, self.sass_path)
        css_path = os.path.join(package_dir, self.css_path)
        css_files = build_directory(sass_path, css_path).values()
        return frozenset(os.path.join(self.css_path, filename)
                         for filename in css_files)

    def build_one(self, package_dir, filename):
        """Builds one SASS/SCSS file.

        :param package_dir: the path of package directory
        :type package_dir: :class:`basestring`
        :param filename: the filename of SASS/SCSS source to compile
        :type filename: :class:`basestring`
        :returns: the filename of compiled CSS
        :rtype: :class:`basestring`

        """
        sass_filename, css_filename = self.resolve_filename(
            package_dir, filename)
        root_path = os.path.join(package_dir, self.sass_path)
        css = compile(filename=sass_filename, include_paths=[root_path])
        css_path = os.path.join(package_dir, self.css_path, css_filename)
        with open(css_path, 'w') as f:
            f.write(css)
        return css_filename
