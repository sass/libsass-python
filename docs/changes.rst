Changelog
=========

Version 0.2.1
-------------

To be released.

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
