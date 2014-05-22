libsass
=======

This package provides a simple Python extension module :mod:`sass` which is
binding Libsass_ (written in C/C++ by Hampton Catlin and Aaron Leung).
It's very straightforward and there isn't any headache related Python
distribution/deployment.  That means you can add just ``libsass`` into
your :file:`setup.py`'s ``install_requires`` list or :file:`requirements.txt`
file.

It currently supports CPython 2.6, 2.7, 3.3, 3.4, and PyPy 2.2!

.. _SASS: http://sass-lang.com/
.. _Libsass: https://github.com/hcatlin/libsass


Install
-------

It's available on PyPI_, so you can install it using :program:`easy_install`
or :program:`pip`:

.. sourcecode:: console

   $ easy_install libsass

.. _PyPI: http://pypi.python.org/pypi/libsass


Example
-------

>>> import sass
>>> sass.compile(string='a { b { color: blue; } }')
'a b {\n  color: blue; }\n'


User's Guide
------------

.. toctree::
   :maxdepth: 2

   frameworks/flask
   changes


References
----------

.. toctree::
   :maxdepth: 2

   sassc
   sass
   sassutils


Credit
------

Hong Minhee wrote this Python binding of Libsass_.

Hampton Catlin and Aaron Leung wrote Libsass_, which is portable C/C++
implementation of SASS_.

Hampton Catlin originally designed SASS_ language and wrote the first
reference implementation of it in Ruby.

The above three softwares are all distributed under `MIT license`_.

.. _MIT license: http://mit-license.org/


Open source
-----------

GitHub (Git repository + issues)
   https://github.com/dahlia/libsass-python

Travis CI
   https://travis-ci.org/dahlia/libsass-python

   .. image:: https://travis-ci.org/dahlia/libsass-python.svg?branch=python
      :target: https://travis-ci.org/dahlia/libsass-python
      :alt: Build Status

Coveralls (Test coverage)
   https://coveralls.io/r/dahlia/libsass-python

   .. image:: https://img.shields.io/coveralls/dahlia/libsass-python.svg
      :target: https://coveralls.io/r/dahlia/libsass-python
      :alt: Coverage Status

PyPI
   https://pypi.python.org/pypi/libsass

   .. image:: https://img.shields.io/pypi/v/libsass.svg
      :target: https://pypi.python.org/pypi/libsass
      :alt: The latest PyPI release

Changelog
   :doc:`changes`


Indices and tables
------------------

- :ref:`genindex`
- :ref:`modindex`
- :ref:`search`
