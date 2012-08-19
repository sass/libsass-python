.. module:: sass

:mod:`sass` --- Binding of ``libsass``
======================================

This simple C extension module provides a very simple binding of ``libsass``,
which is written in C/C++.  It contains only one function and one exception
type.

>>> import sass
>>> sass.compile(string='a { b { color: blue; } }')
'a b {\n  color: blue; }\n'

.. function:: compile(string, filename, output_style, include_paths, image_path)

   It takes a source ``string`` or a ``filename`` and returns the compiled
   CSS string.

   :param string: SASS source code to compile.  it's exclusive to
                  ``filename`` parameter
   :type string: :class:`str`
   :param filename: the filename of SASS source code to compile.
                    it's exclusive to ``string`` parameter
   :type filename: :class:`str`
   :param output_style: an optional coding style of the compiled result.
                        choose one in: ``'nested'`` (default), ``'expanded'``,
                        ``'compact'``, ``'compressed'``
   :type output_style: :class:`str`
   :param include_paths: an optional list of paths to find ``@import``\ ed
                         SASS/CSS source files
   :type include_paths: :class:`collections.Sequence`, :class:`str`
   :param image_path: an optional path to find images
   :type image_path: :class:`str`
   :returns: the compiled CSS string
   :rtype: :class:`str`
   :raises sass.CompileError: when it fails for any reason
                              (for example the given SASS has broken syntax)
   :raises exceptions.IOError: when the ``filename`` doesn't exist or
                               cannot be read

.. exception:: CompileError

   The exception type that is raised by :func:`compile()`.  It is a subtype
   of :exc:`exceptions.ValueError`.
