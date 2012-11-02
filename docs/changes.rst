Changelog
=========

Version 0.2.4
-------------

To be released.

- Added :mod:`sassc` CLI executable script.
- Added :const:`sass.OUTPUT_STYLES` constant map.


Version 0.2.3
-------------

Released on October 24, 2012.

- :mod:`sassutils.distutils`: Prevent double monkey patch of ``sdist``.
- Merged upstream changes of libsass.


Version 0.2.2
-------------

Released on September 28, 2012.

- Fixed a link error on PyPy and Linux.
- Fixed build errors on Windows.


Version 0.2.1
-------------

Released on September 12, 2012.

- Support Windows.


Version 0.2.0
-------------

Released on August 24, 2012.

- Added new :mod:`sassutils` package.

  - Added :mod:`sassutils.builder` module to build the whole directory
    at a time.
  - Added :mod:`sassutils.distutils` module for :mod:`distutils` and
    :mod:`setuptools` integration.
  - Added :mod:`sassutils.wsgi` module which provides a development-purpose
    WSGI middleware.

- Added :class:`~sassutils.distutils.build_sass` command for
  :mod:`distutils`/:mod:`setuptools`.


Version 0.1.1
-------------

Released on August 18, 2012.

- Fixed segmentation fault for reading ``filename`` which does not exist.
  Now it raises a proper ``exceptions.IOError`` exception.


Version 0.1.0
-------------

Released on August 17, 2012.  Initial version.
