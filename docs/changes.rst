Changelog
=========

Version 0.6.1
-------------

To be released.

- Follow up the libsass upstream: :upcommit:`3.0.1` ---
  See the `release note`__ of Libsass.

__ https://github.com/sass/libsass/releases/tag/3.0.1


Version 0.6.0
-------------

Released on October 27, 2014.

Note that since libsass-python 0.6.0 (and libsass 3.0) it requires C++11
to compile.  It means you need GCC (G++) 4.8+, LLVM Clang 3.3+, or
Visual Studio 2013+.

- Follow up the libsass upstream: :upcommit:`3.0` --- See the `release note`__
  of Libsass.

  - Decent extends support
  - Basic Sass Maps Support 
  - Better UTF-8 Support
  - ``call()`` function
  - Better Windows Support
  - Spec Enhancements

- Added missing `partial import`_ support.  [:issue:`27` by item4]
- :const:`~sass.SOURCE_COMMENTS` became deprecated.
- :func:`sass.compile()`'s parameter ``source_comments`` now can take only
  :const:`bool` instead of :const:`str`.  String values like ``'none'``,
  ``'line_numbers'``, and ``'map'`` become deprecated, and will be obsolete
  soon.
- :func:`~sassutils.builder.build_directory()` function has a new optional
  parameter ``output_style``.
- :meth:`~sassutils.builder.Build.build()` method has a new optional
  parameter ``output_style``.
- Added ``--output-style``/``-s`` option to
  :class:`~sassutils.distutils.build_sass` command.  [:issue:`25`]

__ https://github.com/sass/libsass/releases/tag/3.0
.. _partial import: http://sass-lang.com/documentation/file.SASS_REFERENCE.html#partials


Version 0.5.1
-------------

Released on September 23, 2014.

- Fixed a bug that :class:`~sassutils.wsgi.SassMiddleware` yielded
  :class:`str` instead of :class:`bytes` on Python 3.
- Fixed several Unicode-related bugs on Windows.
- Fixed a bug that :func:`~sassutils.builder.build_directory()`,
  :class:`~sassutils.wsgi.SassMiddleware`, and
  :class:`~sassutils.distutils.build_sass` don't recursively build
  subdirectories.


Version 0.5.0
-------------

Released on June 6, 2014.

- Follow up the libsass upstream: :upcommit:`v2.0` ---
  See the `release note`__ of Libsass.

  - Added indented syntax support (:file:`*.sass` files).
  - Added expanded selector support (BEM).
  - Added string functions.
  - Fixed UTF-8 support.
  - Backward incompatibility: broken extends.

__ https://github.com/hcatlin/libsass/releases/tag/v2.0


Unstable version 0.4.2.20140529.cd3ee1cbe3
------------------------------------------

Released on May 29, 2014.

- Version scheme changed to use periods (``.``) instead of hyphens (``-``)
  due to setuptools seems to treat hyphens special.
- Fixed malformed packaging that doesn't correctly preserve the package name
  and version.


Unstable Version 0.4.2-20140528-cd3ee1cbe3
------------------------------------------

Released on May 28, 2014.

- Follow up the libsass upstream:
  :upcommit:`cd3ee1cbe34d5316eb762a43127a3de9575454ee`.


Version 0.4.2
-------------

Released on May 22, 2014.

- Fixed build failing on Mac OS X 10.8 or earlier.  [:issue:`19`]
- Fixed :exc:`UnicodeEncodeError` that :meth:`Manifest.build_one()
  <sassutils.builder.Manifest.build_one>` method rises when the input source
  contains any non-ASCII Unicode characters.


Version 0.4.1
-------------

Released on May 20, 2014.

- Fixed :exc:`UnicodeEncodeError` that rise when the input source contains
  any non-ASCII Unicode characters.


Version 0.4.0
-------------

Released on May 6, 2014.

- :program:`sassc` has a new :option:`-w <sassc -w>`/:option:`--watch
  <sassc --watch>` option.
- Expose source maps support:

  - :program:`sassc` has a new :option:`-m <sassc -m>`/:option:`-g
    <sassc -g>`/:option:`--sourcemap <sassc --sourcemap>` option.
  - :class:`~sassutils.wsgi.SassMiddleware` now also creates source map files
    with filenames followed by :file:`.map` suffix.
  - :meth:`Manifest.build_one() <sassutils.builder.Manifest.build_one>` method
    has a new ``source_map`` option.  This option builds also a source map
    file with the filename followed by :file:`.map` suffix.
  - :func:`sass.compile()` has a new optional parameter ``source_comments``.
    It can be one of :const:`sass.SOURCE_COMMENTS` keys.  It also has
    a new parameter ``source_map_filename`` which is required only when
    ``source_comments='map'``.

- Fixed Python 3 incompatibility of :program:`sassc` program.
- Fixed a bug that multiple ``include_paths`` doesn't work on Windows.


Version 0.3.0
-------------

Released on February 21, 2014.

- Added support for Python 3.3.  [:issue:`7`]
- Dropped support for Python 2.5.
- Fixed build failing on Mac OS X.
  [:issue:`4`, :issue:`5`, :issue:`6` by Hyungoo Kang]
- Now builder creates target recursive subdirectories even if it doesn't
  exist yet, rather than siliently fails.
  [:issue:`8`, :issue:`9` by Philipp Volguine]
- Merged recent changes from libsass :upcommit:`v1.0.1`: `57a2f62--v1.0.1`_.
            
  - Supports `variable arguments`_.
  - Supports sourcemaps.

.. _57a2f62--v1.0.1: https://github.com/hcatlin/libsass/compare/57a2f627b4d2fbd3cf1913b241f1d5aa31e35580...v1.0.1
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
