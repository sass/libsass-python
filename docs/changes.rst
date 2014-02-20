Changelog
=========

Version 0.3.0
-------------

To be released.

- Added support for Python 3.3.
- Dropped support for Python 2.5.
- Fixed build failing on Mac OS X.
  [:issue:`4`, :issue:`5`, :issue:`6` by Hyungoo Kang]
- Now builder creates target recursive subdirectories even if it doesn't
  exist yet, rather than siliently fails.
  [:issue:`8`, :issue:`9` by Philipp Volguine]
- Merged recent changes from libsass upstream:
  `57a2f62--4ad3577`_.
            
  - Supports `variable arguments`_.

.. _57a2f62--4ad3577: https://github.com/hcatlin/libsass/compare/57a2f627b4d2fbd3cf1913b241f1d5aa31e35580...4ad3577cc4bf36356f166939f02d4a7fafd121e0
.. _variable arguments: http://sass-lang.com/docs/yardoc/file.SASS_CHANGELOG.html#variable_arguments


Version 0.2.4
-------------

Released on December 4, 2012.

- Added :mod:`sassc` CLI executable script.
- Added :const:`sass.OUTPUT_STYLES` constant map.
- Merged recent changes from libsass upstream:
  `e997102--a84b181`__.

__ https://github.com/hcatlin/libsass/compare/e9971023785dabd41aa44f431f603f62b15e6017...a84b181a6e59463c0ac9796ca7fdaf4864f0ad84


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
