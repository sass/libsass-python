libsass: SASS_ for Python
=========================

This package provides a simple Python extension module `sass` which is
binding Libsass_ (written in C/C++ by Hampton Catlin and Aaron Leung).
It's very straightforward and there isn't any headache related Python
distribution/deployment.  That means you can add just ``libsass`` into
your ``setup.py``'s ``install_requires`` list or ``requirements.txt`` file.

It currently supports CPython 2.5, 2.6, 2.7, and PyPy 1.9!

.. _SASS: http://sass-lang.com/
.. _Libsass: https://github.com/hcatlin/libsass


Install
-------

Use ``easy_install`` or ``pip``::

    $ easy_install libsass


Use
---

>>> import sass
>>> print sass.compile(string='a { b { color: blue; } }')
'a b {\n  color: blue; }\n'


``sass.compile()``
------------------

It takes a source ``string`` or a ``filename`` and returns the compiled
CSS string.

``string`` (required)
   The string of SASS source code to compile.  It's exclusive to ``filename``
   parameter.

``filename`` (required)
   The filename of SASS source code to compile.  It's exclusive to ``string``
   parameter.

``output_style`` (optional)
   The coding style of the compiled result.  Choose one in:

   - ``'nested'`` (default)
   - ``'expanded'``
   - ``'compact'``
   - ``'compressed'``

``includes_paths`` (optional)
   The list of paths to find ``@import``\ ed SASS/CSS source files.

``image_path`` (optional)
   The path to find images.


Credit
------

Hong Minhee wrote this Python binding of Libsass_.

Hampton Catlin and Aaron Leung wrote Libsass_, which is portable C/C++
implementation of SASS_.

Hampton Catlin originally designed SASS_ language and wrote the first
reference implementation of it in Ruby.

The above three softwares are all distributed under `MIT license`_.

.. _MIT license: http://mit-license.org/


Changelog
---------

Version 0.1.0
'''''''''''''

Released on August 17, 2012.  Initial version.
