libsass: SASS_ for Python
=========================

.. image:: https://img.shields.io/pypi/v/libsass.svg
   :target: https://pypi.python.org/pypi/libsass
   :alt: The latest PyPI release

.. image:: https://travis-ci.org/dahlia/libsass-python.svg?branch=python
   :target: https://travis-ci.org/dahlia/libsass-python
   :alt: Build Status

.. image:: https://img.shields.io/coveralls/dahlia/libsass-python.svg
   :target: https://coveralls.io/r/dahlia/libsass-python
   :alt: Coverage Status

This package provides a simple Python extension module ``sass`` which is
binding Libsass_ (written in C/C++ by Hampton Catlin and Aaron Leung).
It's very straightforward and there isn't any headache related Python
distribution/deployment.  That means you can add just ``libsass`` into
your ``setup.py``'s ``install_requires`` list or ``requirements.txt`` file.
Need no Ruby nor Node.js.

It currently supports CPython 2.6, 2.7, 3.3, 3.4, and PyPy 1.9+!

.. _SASS: http://sass-lang.com/
.. _Libsass: https://github.com/hcatlin/libsass


Install
-------

It's available on PyPI_, so you can install it using ``pip`` (or
``easy_install``):

.. code-block:: console

   $ pip install libsass

Every release of libsass-python uses the most recent release of Libsass_.
If you want bleeding edge features of libsass master, try installing
libsass-unstable_ package instead:

.. code-block:: console

  $ pip install libsass-unstable

.. _PyPI: https://pypi.python.org/pypi/libsass
.. _libsass-unstable: https://pypi.python.org/pypi/libsass-unstable


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

http://dahlia.kr/libsass-python/

You can build the docs by yourself:

.. code-block:: console

   $ cd docs/
   $ make html

The built docs will go to ``docs/_build/html/`` directory.


Credit
------

Hong Minhee wrote this Python binding of Libsass_.

Hampton Catlin and Aaron Leung wrote Libsass_, which is portable C/C++
implementation of SASS_.

Hampton Catlin originally designed SASS_ language and wrote the first
reference implementation of it in Ruby.

The above three softwares are all distributed under `MIT license`_.

.. _MIT license: http://mit-license.org/
