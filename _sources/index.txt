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

It's available on PyPI_, so you can install it using :program:`pip`:

.. code-block:: console

   $ pip install libsass

.. note::

   Every release of libsass-python uses the most recent release of Libsass_.
   If you want bleeding edge features of libsass master, try installing
   libsass-unstable_ package instead:

   .. code-block:: console

      $ pip install libsass-unstable

.. _PyPI: https://pypi.python.org/pypi/libsass
.. _libsass-unstable: https://pypi.python.org/pypi/libsass-unstable


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

AppVeyor (CI for Windows)
   https://ci.appveyor.com/project/dahlia/libsass-python

   .. image:: https://ci.appveyor.com/api/projects/status/yghrs9jw7b67c0ia/branch/python?svg=true
      :target: https://ci.appveyor.com/project/dahlia/libsass-python
      :alt: Build Status (Windows)

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
