libsass-python: Sass_/SCSS for Python
=====================================

.. image:: https://badge.fury.io/py/libsass.svg
   :alt: PyPI
   :target: https://pypi.org/pypi/libsass/

.. image:: https://github.com/sass/libsass-python/actions/workflows/main.yml/badge.svg
   :target: https://github.com/sass/libsass-python/actions/workflows/main.yml
   :alt: Build Status

.. image:: https://results.pre-commit.ci/badge/github/sass/libsass-python/main.svg
   :target: https://results.pre-commit.ci/latest/github/sass/libsass-python/main
   :alt: pre-commit.ci status

This package provides a simple Python extension module ``sass`` which is
binding LibSass_ (written in C/C++ by Hampton Catlin and Aaron Leung).
It's very straightforward and there isn't any headache related to Python
distribution/deployment.  That means you can add just ``libsass`` into
your ``setup.py``'s ``install_requires`` list or ``requirements.txt`` file.
No need for Ruby nor Node.js.

It currently supports CPython 3.7+, and PyPy 3!

.. _Sass: https://sass-lang.com/
.. _LibSass: https://github.com/sass/libsass


Features
--------

- You don't need any Ruby/Node.js stack at all, for development or deployment
  either.
- Fast. (LibSass_ is written in C++.)
- Simple API.  See the below example code for details.
- Custom functions.
- ``@import`` callbacks.
- Support both tabbed (Sass) and braces (SCSS) syntax.
- WSGI middleware for ease of development.
  It automatically compiles Sass/SCSS files for each request.
- ``setuptools``/``distutils`` integration.
  You can build all Sass/SCSS files using
  ``setup.py build_sass`` command.
- Works also on PyPy.
- Provides prebuilt wheel_ binaries for Linux, Windows, and Mac.

.. _wheel: https://www.python.org/dev/peps/pep-0427/


Install
-------

It's available on PyPI_, so you can install it using ``pip`` (or
``easy_install``):

.. code-block:: console

   $ pip install libsass

.. note::

   libsass requires some features introduced by the recent C++ standard.
   You need a C++ compiler that support those features.
   See also libsass project's README_ file.

.. _PyPI: https://pypi.org/pypi/libsass/
.. _README: https://github.com/sass/libsass#readme


.. _example:

Example
-------

.. code-block:: pycon

   >>> import sass
   >>> print sass.compile(string='a { b { color: blue; } }')
   a b {
     color: blue; }


Docs
----

There's the user guide manual and the full API reference for ``libsass``:

https://sass.github.io/libsass-python/

You can build the docs by yourself:

.. code-block:: console

   $ cd docs/
   $ make html

The built docs will go to ``docs/_build/html/`` directory.


Credit
------

Hong Minhee wrote this Python binding of LibSass_.

Hampton Catlin and Aaron Leung wrote LibSass_, which is portable C/C++
implementation of Sass_.

Hampton Catlin originally designed Sass_ language and wrote the first
reference implementation of it in Ruby.

The above three are all distributed under `MIT license`_.

.. _MIT license: https://mit-license.org/
