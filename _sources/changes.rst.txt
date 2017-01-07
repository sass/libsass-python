Changelog
=========


Version 0.12.3
--------------

Released on January 7, 2017.

- Follow up the libsass upstream: 3.4.3 --- See the release notes of Libsass
  3.4.3__. [:issue:`178` by Anthony Sottile]

__ https://github.com/sass/libsass/releases/tag/3.4.3


Version 0.12.2
--------------

Released on January 5, 2017.

- Follow up the libsass upstream: 3.4.2 --- See the release notes of Libsass
  3.4.2__. [:issue:`176` by Anthony Sottile]

__ https://github.com/sass/libsass/releases/tag/3.4.2


Version 0.12.1
--------------

Released on December 20, 2016.

- Follow up the libsass upstream: 3.4.1 --- See the release notes of Libsass
  3.4.1__. [:issue:`175` by Anthony Sottile]

__ https://github.com/sass/libsass/releases/tag/3.4.1


Version 0.12.0
--------------

Released on December 10, 2016.

- Follow up the libsass upstream: 3.4.0 --- See the release notes of Libsass
  3.4.0__. [:issue:`173` by Anthony Sottile]

__ https://github.com/sass/libsass/releases/tag/3.4.0


Version 0.11.2
--------------

Released on October 24, 2016.

- Drop support for python2.6 [:issue:`158` by Anthony Sottile]
- Deprecate `--watch` [:issue:`156` by Anthony Sottile]
- Preserve line endings [:issue:`160` by Anthony Sottile]
- Follow up the libsass upstream: 3.3.6 --- See the release notes of Libsass
  3.3.6__. [:issue:`167` by Anthony Sottile]

__ https://github.com/sass/libsass/releases/tag/3.3.6



Version 0.11.1
--------------

Released on April 22, 2016.

- Follow up the libsass upstream: 3.3.5 --- See the release notes of Libsass
  3.3.5__. [:issue:`148` by Anthony Sottile]

__ https://github.com/sass/libsass/releases/tag/3.3.5

Version 0.11.0
--------------

Released on March 23, 2016.

- Follow up the libsass upstream: 3.3.4 --- See the release notes of Libsass
  3.3.4__. [:issue:`144` by Anthony Sottile]
- Expose libsass version in `sassc --version` and `sass.libsass_version`
  [:issue:`142` :issue:`141` :issue:`140` by Anthony Sottile]
- Fix warning about unused enum on switch [:issue:`127` :issue:`131` by
  Anthony Sottile]
- Sourcemaps no longer imply source comments [:issue:`124` :issue:`130` by
  Tim Tisdall]
- Add `--source-comments` option to `sassc` [:issue:`124` :issue:`130` by
  Anthony Sottile]
- Improve formatting of `CompileError` under python3 [:issue:`123` by Anthony
  Sottile]
- Raise when compiling a directory which does not exist [:issue:`116`
  :issue:`119` by Anthony Sottile]

__ https://github.com/sass/libsass/releases/tag/3.3.4

Version 0.10.1
--------------

Released on January 29, 2016.

- Follow up the libsass upstream: 3.3.3 --- See the release notes of Libsass
  3.3.3__. [by Anthony Sottile]
- Allow -t for style like sassc [:issue:`98` by Anthony Sottile]

__ https://github.com/sass/libsass/releases/tag/3.3.3

Version 0.10.0
--------------

Released on December 15, 2015.

- Support custom import callbacks [:issue:`81` by Alice Zoë Bevan–McGregor,
  Anthony Sottile]
- Disallow arbitrary kwargs in compile() [:issue:`109` by Anthony Sottile]

Version 0.9.3
-------------

Released on December 03, 2015.

- Support "indented" SASS compilation [:issue:`41` by Alice Zoë Bevan–McGregor]
- Fix wheels on windows [:issue:`28` :issue:`49` by Anthony Sottile]

Version 0.9.2
-------------

Released on November 12, 2015.

- Follow up the libsass upstream: 3.3.2 --- See the release notes of Libsass
  3.3.2__. [by Anthony Sottile]
- Require VS 2015 to build on windows [:issue:`99` by Anthony Sottile]

__ https://github.com/sass/libsass/releases/tag/3.3.2

Version 0.9.1
-------------

Released on October 29, 2015.

- Follow up the libsass upstream: 3.3.1 --- See the release notes of Libsass
  3.3.1__. [by Anthony Sottile]

__ https://github.com/sass/libsass/releases/tag/3.3.1


Version 0.9.0
-------------

Released on October 28, 2015.

- Fix a bug with writing UTF-8 to a file [:issue:`72` by Caleb Ely]
- Fix a segmentation fault on ^C [:issue:`87` by Anthony Sottile]
- Follow up the libsass upstream: 3.3.0 --- See the release notes of Libsass
  3.3.0__. [:issue:`96` by Anthony Sottile]

__ https://github.com/sass/libsass/releases/tag/3.3.0


Version 0.8.3
-------------

Released on August 2, 2015.

- Follow up the libsass upstream: 3.2.5 --- See the release notes of Libsass
  3.2.5__.  [:issue:`79`, :issue:`80` by Anthony Sottile]
- Fixed a bug that :file:`*.sass` files were ignored.
  [:issue:`78` by Guilhem MAS-PAITRAULT]

__ https://github.com/sass/libsass/releases/tag/3.2.5


Version 0.8.2
-------------

Released on May 19, 2015.

- Follow up the libsass upstream: 3.2.4 --- See the release notes of Libsass
  3.2.3__, and 3.2.4__.  [:issue:`69` by Anthony Sottile]
- The default value of :class:`~sassutils.wsgi.SassMiddleware`'s
  ``error_status`` parameter was changed from ``'500 Internal Server Error'``
  to ``'200 OK'`` so that Mozilla Firefox can render the error message well.
  [:issue:`67`, :issue:`68`, :issue:`70` by zxv]

__ https://github.com/sass/libsass/releases/tag/3.2.3
__ https://github.com/sass/libsass/releases/tag/3.2.4


Version 0.8.1
-------------

Released on May 14, 2015.

- Fixed a bug that there was no ``'expanded'`` in :const:`sass.OUTPUT_STYLES`
  but ``'expected'`` instead which is a typo.  [:issue:`66` by Triangle717]
- Fixed broken FreeBSD build.  [:issue:`65` by Toshiharu Moriyama]


Version 0.8.0
-------------

Released on May 3, 2015.

- Follow up the libsass upstream: 3.2.2 --- See the release notes of Libsass
  3.2.0__, 3.2.1__, and 3.2.2__.
  [:issue:`61`, :issue:`52`, :issue:`56`, :issue:`58`, :issue:`62`, :issue:`64`
  by Anthony Sottile]

  - Compact and expanded output styles  [:issue:`37`]
  - Strings and interpolation closer to Ruby Sass
  - The correctness of the generated sourcemap files
  - Directive buddling
  - Full support for the ``@at-root`` directive
  - Full support for ``!global`` variable scoping

- Now underscored files are ignored when compiling a directory.
  [:issue:`57` by Anthony Sottile]
- Fixed broken FreeBSD build.  [:issue:`34`, :issue:`60` by Ilya Baryshev]
- :class:`~sassutils.wsgi.SassMiddleware` became to log syntax errors
  if exist during compilation to ``sassutils.wsgi.SassMiddleware`` logger
  with level ``ERROR``.  [:issue:`42`]

__ https://github.com/sass/libsass/releases/tag/3.2.0
__ https://github.com/sass/libsass/releases/tag/3.2.1
__ https://github.com/sass/libsass/releases/tag/3.2.2


Version 0.7.0
-------------

Released on March 6, 2015.

Anthony Sottile contributed to the most of this release.  Huge thanks to him!

- Follow up the libsass upstream: 3.1.0 --- See the `release note`__ of Libsass.
  [:issue:`38`, :issue:`43` by Anthony Sottile]

  - Custom functions and imports
  - Decrementing in ``@for`` loops
  - ``@debug`` and ``@error``
  - ``not`` operator
  - ``nth()`` for maps
  - ``inspect()``
  - ``feature-exists()``
  - ``unique-id()``
  - ``random()``

- Added custom functions support.  [:issue:`13`, :issue:`44` by Anthony Sottile]

  - Added :class:`sass.SassFunction` class.
  - Added ``custom_functions`` parameter to :func:`sass.compile()` function.
  - Added data types for custom functions:

    - :class:`sass.SassNumber`
    - :class:`sass.SassColor`
    - :class:`sass.SassList`
    - :class:`sass.SassMap`
    - :class:`sass.SassError`
    - :class:`sass.SassWarning`

- Added ``precision`` parameter to :func:`sass.compile()` function.
  [:issue:`39` by Andrea Stagi]
- :program:`sassc` has a new :option:`-p <sassc -p>`/:option:`--precision
  <sassc --precision>` option.  [:issue:`39` by Andrea Stagi]

__ https://github.com/sass/libsass/releases/tag/3.1.0


Version 0.6.2
-------------

Released on November 25, 2014.

Although 0.6.0--0.6.1 have needed GCC (G++) 4.8+, LLVM Clang 3.3+,
now it became back to only need GCC (G++) 4.6+, LLVM Clang 2.9+,
or Visual Studio 2013 Update 4+.

- Follow up the libsass upstream: 3.0.2 --- See the `release note`__ of libsass.
  [:issue:`33` by Rodolphe Pelloux-Prayer]
- Fixed a bug that :program:`sassc --watch` crashed when a file is not
  compilable on the first try.  [:issue:`32` by Alan Justino da Silva]
- Fixed broken build on Windows.

__ https://github.com/sass/libsass/releases/tag/3.0.2


Version 0.6.1
-------------

Released on November 6, 2014.

- Follow up the libsass upstream: 3.0.1 --- See the `release note`__ of Libsass.
- Fixed a bug that :class:`~sassutils.wsgi.SassMiddleware` never closes
  the socket on some WSGI servers e.g. ``eventlet.wsgi``.

__ https://github.com/sass/libsass/releases/tag/3.0.1


Version 0.6.0
-------------

Released on October 27, 2014.

Note that since libsass-python 0.6.0 (and libsass 3.0) it requires C++11
to compile.  Although 0.6.2 became back to only need GCC (G++) 4.6+,
LLVM Clang 2.9+, from 0.6.0 to 0.6.1 you need GCC (G++) 4.8+, LLVM Clang 3.3+,
or Visual Studio 2013 Update 4+.

- Follow up the libsass upstream: 3.0 --- See the `release note`__ of Libsass.

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

- Follow up the libsass upstream: 2.0 --- See the `release note`__ of Libsass.

  - Added indented syntax support (:file:`*.sass` files).
  - Added expanded selector support (BEM).
  - Added string functions.
  - Fixed UTF-8 support.
  - Backward incompatibility: broken extends.

__ https://github.com/sass/libsass/releases/tag/v2.0


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
- Merged recent changes from libsass 1.0.1: `57a2f62--v1.0.1`_.
            
  - Supports `variable arguments`_.
  - Supports sourcemaps.

.. _57a2f62--v1.0.1: https://github.com/sass/libsass/compare/57a2f627b4d2fbd3cf1913b241f1d5aa31e35580...v1.0.1
.. _variable arguments: http://sass-lang.com/docs/yardoc/file.SASS_CHANGELOG.html#variable_arguments


Version 0.2.4
-------------

Released on December 4, 2012.

- Added :mod:`sassc` CLI executable script.
- Added :const:`sass.OUTPUT_STYLES` constant map.
- Merged recent changes from libsass upstream:
  `e997102--a84b181`__.

__ https://github.com/sass/libsass/compare/e9971023785dabd41aa44f431f603f62b15e6017...a84b181a6e59463c0ac9796ca7fdaf4864f0ad84


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
