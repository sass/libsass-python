""":mod:`sass` --- Binding of ``libsass``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This simple C extension module provides a very simple binding of ``libsass``,
which is written in C/C++.  It contains only one function and one exception
type.

>>> import sass
>>> sass.compile(string='a { b { color: blue; } }')
'a b {\n  color: blue; }\n'

"""
import collections
import os
import os.path
import sys

from six import string_types, text_type

from _sass import (OUTPUT_STYLES, SOURCE_COMMENTS, compile_dirname,
                   compile_filename, compile_string)

__all__ = ('MODES', 'OUTPUT_STYLES', 'SOURCE_COMMENTS', 'CompileError',
           'and_join', 'compile')
__version__ = '0.4.2'


#: (:class:`collections.Mapping`) The dictionary of output styles.
#: Keys are output name strings, and values are flag integers.
OUTPUT_STYLES = OUTPUT_STYLES

#: (:class:`collections.Mapping`) The dictionary of source comments styles.
#: Keys are mode names, and values are corresponding flag integers.
#:
#: .. versionadded:: 0.4.0
SOURCE_COMMENTS = SOURCE_COMMENTS

#: (:class:`collections.Set`) The set of keywords :func:`compile()` can take.
MODES = set(['string', 'filename', 'dirname'])


class CompileError(ValueError):
    """The exception type that is raised by :func:`compile()`.
    It is a subtype of :exc:`exceptions.ValueError`.

    """


def compile(**kwargs):
    """There are three modes of parameters :func:`compile()` can take:
    ``string``, ``filename``, and ``dirname``.

    The ``string`` parameter is the most basic way to compile SASS.
    It simply takes a string of SASS code, and then returns a compiled
    CSS string.

    :param string: SASS source code to compile.  it's exclusive to
                   ``filename`` and ``dirname`` parameters
    :type string: :class:`str`
    :param output_style: an optional coding style of the compiled result.
                         choose one of: ``'nested'`` (default), ``'expanded'``,
                         ``'compact'``, ``'compressed'``
    :type output_style: :class:`str`
    :param source_comments: an optional source comments mode of the compiled
                            result.  choose one of ``'none'`` (default) or
                            ``'line_numbers'``.  ``'map'`` is unavailable for
                            ``string``
    :type source_comments: :class:`str`
    :param include_paths: an optional list of paths to find ``@import``\ ed
                          SASS/CSS source files
    :type include_paths: :class:`collections.Sequence`, :class:`str`
    :param image_path: an optional path to find images
    :type image_path: :class:`str`
    :returns: the compiled CSS string
    :rtype: :class:`str`
    :raises sass.CompileError: when it fails for any reason
                               (for example the given SASS has broken syntax)

    The ``filename`` is the most commonly used way.  It takes a string of
    SASS filename, and then returns a compiled CSS string.

    :param filename: the filename of SASS source code to compile.
                     it's exclusive to ``string`` and ``dirname`` parameters
    :type filename: :class:`str`
    :param output_style: an optional coding style of the compiled result.
                         choose one of: ``'nested'`` (default), ``'expanded'``,
                         ``'compact'``, ``'compressed'``
    :type output_style: :class:`str`
    :param source_comments: an optional source comments mode of the compiled
                            result.  choose one of ``'none'`` (default),
                            ``'line_numbers'``, ``'map'``.
                            if ``'map'`` is used it requires
                            ``source_map_filename`` argument as well and
                            returns a (compiled CSS string,
                            source map string) pair instead of a string
    :type source_comments: :class:`str`
    :param source_map_filename: indicate the source map output filename.
                                it's only available and required
                                when ``source_comments`` is ``'map'``.
                                note that it will ignore all other parts of
                                the path except for its basename
    :type source_map_filename: :class:`str`
    :param include_paths: an optional list of paths to find ``@import``\ ed
                          SASS/CSS source files
    :type include_paths: :class:`collections.Sequence`, :class:`str`
    :param image_path: an optional path to find images
    :type image_path: :class:`str`
    :returns: the compiled CSS string, or a pair of the compiled CSS string
              and the source map string if ``source_comments='map'``
    :rtype: :class:`str`, :class:`tuple`
    :raises sass.CompileError: when it fails for any reason
                               (for example the given SASS has broken syntax)
    :raises exceptions.IOError: when the ``filename`` doesn't exist or
                                cannot be read

    The ``dirname`` is useful for automation.  It takes a pair of paths.
    The first of the ``dirname`` pair refers the source directory, contains
    several SASS source files to compiled.  SASS source files can be nested
    in directories.  The second of the pair refers the output directory
    that compiled CSS files would be saved.  Directory tree structure of
    the source directory will be maintained in the output directory as well.
    If ``dirname`` parameter is used the function returns :const:`None`.

    :param dirname: a pair of ``(source_dir, output_dir)``.
                    it's exclusive to ``string`` and ``filename``
                    parameters
    :type dirname: :class:`tuple`
    :param output_style: an optional coding style of the compiled result.
                         choose one of: ``'nested'`` (default), ``'expanded'``,
                         ``'compact'``, ``'compressed'``
    :type output_style: :class:`str`
    :param source_comments: an optional source comments mode of the compiled
                            result.  choose one of ``'none'`` (default) or
                            ``'line_numbers'``.  ``'map'`` is unavailable for
                            ``dirname``
    :type source_comments: :class:`str`
    :param include_paths: an optional list of paths to find ``@import``\ ed
                          SASS/CSS source files
    :type include_paths: :class:`collections.Sequence`, :class:`str`
    :param image_path: an optional path to find images
    :type image_path: :class:`str`
    :raises sass.CompileError: when it fails for any reason
                               (for example the given SASS has broken syntax)

    .. versionadded:: 0.4.0
       Added ``source_comments`` and ``source_map_filename`` parameters.

    """
    modes = set()
    for mode_name in MODES:
        if mode_name in kwargs:
            modes.add(mode_name)
    if not modes:
        raise TypeError('choose one at least in ' + and_join(MODES))
    elif len(modes) > 1:
        raise TypeError(and_join(modes) + ' are exclusive each other; '
                        'cannot be used at a time')
    output_style = kwargs.pop('output_style', 'nested')
    if not isinstance(output_style, string_types):
        raise TypeError('output_style must be a string, not ' +
                        repr(output_style))
    try:
        output_style = OUTPUT_STYLES[output_style]
    except KeyError:
        raise CompileError('{0} is unsupported output_style; choose one of {1}'
                           ''.format(output_style, and_join(OUTPUT_STYLES)))
    source_comments = kwargs.pop('source_comments', 'none')
    if not isinstance(source_comments, string_types):
        raise TypeError('source_comments must be a string, not ' +
                        repr(source_comments))
    if 'filename' not in modes and source_comments == 'map':
        raise CompileError('source_comments="map" is only available with '
                           'filename= keyword argument since it has to be '
                           'aware of it')
    try:
        source_comments = SOURCE_COMMENTS[source_comments]
    except KeyError:
        raise CompileError(
            '{0} is unsupported source_comments; choose one of '
            '{1}'.format(source_comments, and_join(SOURCE_COMMENTS))
        )
    fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
    try:
        source_map_filename = kwargs.pop('source_map_filename') or b''
    except KeyError:
        if source_comments == SOURCE_COMMENTS['map']:
            raise TypeError('source_comments="map" requires '
                            'source_map_filename argument')
        source_map_filename = b''
    else:
        if source_comments != SOURCE_COMMENTS['map']:
            raise TypeError('source_map_filename is available only with '
                            'source_comments="map"')
        elif not isinstance(source_map_filename, string_types):
            raise TypeError('source_map_filename must be a string, not ' +
                            repr(source_map_filename))
        if isinstance(source_map_filename, text_type):
            source_map_filename = source_map_filename.encode(fs_encoding)
    try:
        include_paths = kwargs.pop('include_paths') or b''
    except KeyError:
        include_paths = b''
    else:
        if isinstance(include_paths, collections.Sequence):
            include_paths = os.pathsep.join(include_paths)
        elif not isinstance(include_paths, string_types):
            raise TypeError('include_paths must be a sequence of strings, or '
                            'a colon-separated (or semicolon-separated if '
                            'Windows) string, not ' + repr(include_paths))
        if isinstance(include_paths, text_type):
            include_paths = include_paths.encode(fs_encoding)
    try:
        image_path = kwargs.pop('image_path')
    except KeyError:
        image_path = b'.'
    else:
        if not isinstance(image_path, string_types):
            raise TypeError('image_path must be a string, not ' +
                            repr(image_path))
        elif isinstance(image_path, text_type):
            image_path = image_path.encode(fs_encoding)
    if 'string' in modes:
        string = kwargs.pop('string')
        if isinstance(string, text_type):
            string = string.encode('utf-8')
        s, v = compile_string(string,
                              output_style, source_comments,
                              include_paths, image_path)
        if s:
            return v.decode('utf-8')
    elif 'filename' in modes:
        filename = kwargs.pop('filename')
        if not isinstance(filename, string_types):
            raise TypeError('filename must be a string, not ' + repr(filename))
        elif not os.path.isfile(filename):
            raise IOError('{0!r} seems not a file'.format(filename))
        elif isinstance(filename, text_type):
            filename = filename.encode(fs_encoding)
        s, v, source_map = compile_filename(
            filename,
            output_style, source_comments,
            include_paths, image_path, source_map_filename
        )
        if s:
            v = v.decode('utf-8')
            if source_map_filename:
                v = v, source_map.decode('utf-8')
            return v
    elif 'dirname' in modes:
        try:
            search_path, output_path = kwargs.pop('dirname')
        except ValueError:
            raise ValueError('dirname must be a pair of (source_dir, '
                             'output_dir)')
        else:
            if isinstance(search_path, text_type):
                search_path = search_path.encode(fs_encoding)
            if isinstance(output_path, text_type):
                output_path = output_path.encode(fs_encoding)
        s, v = compile_dirname(search_path, output_path,
                               output_style, source_comments,
                               include_paths, image_path)
        if s:
            return
    else:
        raise TypeError('something went wrong')
    assert not s
    raise CompileError(v)


def and_join(strings):
    """Join the given ``strings`` by commas with last `' and '` conjuction.

    >>> and_join(['Korea', 'Japan', 'China', 'Taiwan'])
    'Korea, Japan, China, and Taiwan'

    :param strings: a list of words to join
    :type string: :class:`collections.Sequence`
    :returns: a joined string
    :rtype: :class:`str`, :class:`basestring`

    """
    last = len(strings) - 1
    if last == 0:
        return strings[0]
    elif last < 0:
        return ''
    iterator = enumerate(strings)
    return ', '.join('and ' + s if i == last else s for i, s in iterator)
