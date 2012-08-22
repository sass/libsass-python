""":mod:`sassutils.distutils` --- :mod:`setuptools`/:mod:`distutils` integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides extensions (and some magical monkey-patches, sorry)
of the standard :mod:`distutils` and :mod:`setuptools` (now it's named
Distribute) for libsass.

To use this, add ``libsass`` into ``setup_requires`` (not ``install_requires``)
option of the :file:`setup.py` script::

    from setuptools import setup

    setup(
        # ...,
        setup_requires=['libsass >= 0.2.0']
    )

It will adds :class:`build_sass` command to the :file:`setup.py` script:

.. sourcecode:: console

   $ python setup.py build_sass

This commands builds SASS/SCSS files to compiled CSS files of the project
and makes the package archive (made by :class:`~distutils.command.sdist.sdist`,
:class:`~distutils.command.bdist.bdist`, and so on) to include these compiled
CSS files.

To set the directory of SASS/SCSS source files and the directory to
store compiled CSS files, specify ``sass_manifests`` option::

    from setuptools import find_packages, setup

    setup(
        name='YourPackage',
        packages=find_packages(),
        sass_manifests={
            'your.webapp': ('static/sass', 'static/css')
        },
        setup_requires=['libsass >= 0.2.0']
    )

The option should be a mapping of package names to pairs of paths, e.g.::

    {
        'package': ('static/sass', 'static/css'),
        'package.name': ('static/scss', 'static')
    }

"""
from __future__ import absolute_import

import collections
import distutils.errors
import distutils.log
import distutils.util
import functools
import os.path

from setuptools import Command
from setuptools.command.sdist import sdist

from .builder import build_directory

__all__ = 'Manifest', 'build_sass', 'validate_manifests'


def validate_manifests(dist, attr, value):
    """Verifies that ``value`` is an expected mapping of package to
    :class:`Manifest`.

    """
    error = distutils.errors.DistutilsSetupError(
        "value must be a mapping object like: {'package.name': "
        "sassutils.distutils.Manifest('sass/path')}, or as shorten form: "
        "{'package.name': ('sass/path', 'css/path'}), not " +
        repr(value)
    )
    if not isinstance(value, collections.Mapping):
        raise error
    for package_name, manifest in value.items():
        if not isinstance(package_name, basestring):
            raise error
        elif not isinstance(manifest, (basestring, tuple, Manifest)):
            raise error
        elif isinstance(manifest, tuple) and len(manifest) != 2:
            raise error


class Manifest(object):
    """Building manifest of SASS/SCSS.

    :param sass_path: the path of the directory that contains SASS/SCSS
                      source files
    :type sass_path: :class:`basestring`
    :param css_path: the path of the directory to store compiled CSS
                     files
    :type css_path: :class:`basestring`

    """

    def __init__(self, sass_path, css_path=None):
        if not isinstance(sass_path, basestring):
            raise TypeError('sass_path must be a string, not ' +
                            repr(sass_path))
        if css_path is None:
            css_path = sass_path
        elif not isinstance(css_path, basestring):
            raise TypeError('css_path must be a string, not ' +
                            repr(css_path))
        self.sass_path = sass_path
        self.css_path = css_path

    def build(self, package_dir):
        """Builds the SASS/CSS files in the specified :attr:`sass_path`.
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


class build_sass(Command):
    """Builds SASS/SCSS files to CSS files."""

    descriptin = __doc__
    user_options = []

    def initialize_options(self):
        self.package_dir = None

    def finalize_options(self):
        self.package_dir = {}
        if self.distribution.package_dir:
            self.package_dir = {}
            for name, path in self.distribution.package_dir.items():
                self.package_dir[name] = distutils.util.convert_path(path)

    def run(self):
        manifests = self.normalize_manifests()
        package_data = self.distribution.package_data
        data_files = self.distribution.data_files or []
        for package_name, manifest in manifests.items():
            package_dir = self.get_package_dir(package_name)
            distutils.log.info("building '%s' sass", package_name)
            css_files = manifest.build(package_dir)
            map(distutils.log.info, css_files)
            package_data.setdefault(package_name, []).extend(css_files)
            data_files.extend((package_dir, f) for f in css_files)
        self.distribution.package_data = package_data
        self.distribution.data_files = data_files
        self.distribution.has_data_files = lambda: True
        # See the below monkey patch (end of this source code).
        self.distribution.compiled_sass_files = data_files

    def normalize_manifests(self):
        manifests = self.distribution.sass_manifests
        if manifests is None:
            manifests = {}
        for package_name, manifest in manifests.items():
            if isinstance(manifest, Manifest):
                continue
            elif isinstance(manifest, tuple):
                manifest = Manifest(*manifest)
            elif isinstance(manifest, basestring):
                manifest = Manifest(manifest)
            manifests[package_name] = manifest
        self.distribution.sass_manifests = manifests
        return manifests

    def get_package_dir(self, package):
        """Returns the directory, relative to the top of the source
        distribution, where package ``package`` should be found
        (at least according to the :attr:`package_dir` option, if any).

        Copied from :meth:`distutils.command.build_py.get_package_dir()`
        method.

        """
        path = package.split('.')
        if not self.package_dir:
            if path:
                return os.path.join(*path)
            return ''
        tail = []
        while path:
            try:
                pdir = self.package_dir['.'.join(path)]
            except KeyError:
                tail.insert(0, path[-1])
                del path[-1]
            else:
                tail.insert(0, pdir)
                return os.path.join(*tail)
        else:
            pdir = self.package_dir.get('')
            if pdir is not None:
                tail.insert(0, pdir)
            if tail:
                return os.path.join(*tail)
            return ''


# Does monkey-patching the setuptools.command.sdist.sdist.check_readme()
# method to include compiled SASS files as data files.
@functools.wraps(sdist.check_readme)
def check_readme(self):
    try:
        files = self.distribution.compiled_sass_files
    except AttributeError:
        pass
    else:
        self.filelist.extend(os.path.join(*pair) for pair in files)
    return self._wrapped_check_readme()
sdist._wrapped_check_readme = sdist.check_readme
sdist.check_readme = check_readme
