libsass
=======

This package provides a simple Python extension module :mod:`sass` which is
binding Libsass_ (written in C/C++ by Hampton Catlin and Aaron Leung).
It's very straightforward and there isn't any headache related Python
distribution/deployment.  That means you can add just ``libsass`` into
your :file:`setup.py`'s ``install_requires`` list or :file:`requirements.txt`
file.

It currently supports CPython 2.5, 2.6, 2.7, and PyPy 1.9!

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


References
----------

.. toctree::
   :maxdepth: 2

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

PyPI
   http://pypi.python.org/pypi/libsass

Changelog
   :doc:`changes`


Indices and tables
------------------

- :ref:`genindex`
- :ref:`modindex`
- :ref:`search`
