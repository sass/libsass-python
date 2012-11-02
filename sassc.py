#!/usr/bin/env python
""":mod:`sassc` --- SassC compliant command line interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This provides SassC_ compliant CLI executable named :program:`sassc`:

.. sourcecode:: console

   $ sassc
   Usage: sassc [options] SCSS_FILE...

There are options as well:

.. option:: -s <style>, --output-style <style>

   Coding style of the compiled result.  The same as :func:`sass.compile()`
   function's ``output_style`` keyword argument.  Default is ``nested``.

.. option:: -I <dir>, --include-path <dir>

   Optional directory path to find ``@import``\ ed (S)CSS files.
   Can be multiply used.

.. option:: -i <dir>, --image-path <dir>

   Path to find images.  Default is the current directory (:file:`./`).

.. option:: -v, --version

   Prints the program version.

.. option:: -h, --help

   Prints the help message.

.. _SassC: https://github.com/hcatlin/sassc

"""
import optparse
import sys

from sass import __version__ as VERSION, OUTPUT_STYLES, CompileError, compile


def main(argv=sys.argv, stdout=sys.stdout, stderr=sys.stderr):
    parser = optparse.OptionParser(usage='%prog [options] SCSS_FILE...',
                                   version='%prog ' + VERSION)
    output_styles = list(OUTPUT_STYLES)
    output_styles = ', '.join(output_styles[:-1]) + ', or ' + output_styles[-1]
    parser.add_option('-s', '--output-style', metavar='STYLE', type='choice',
                      choices=list(OUTPUT_STYLES), default='nested',
                      help='Coding style of the compiled result.  Choose one '
                           'of ' + output_styles + '. [default: %default]')
    parser.add_option('-I', '--include-path', metavar='DIR',
                      dest='include_paths', action='append',
                      help='Path to find "@import"ed (S)CSS source files.  '
                           'Can be multiply used.')
    parser.add_option('-i', '--image-path', metavar='DIR', default='./',
                      help='Path to find images. [default: %default]')
    options, args = parser.parse_args(argv[1:])
    if not args:
        parser.print_usage(stderr)
        print >> stderr, parser.get_prog_name() + ': error:', \
                         'too few arguments'
        return 2
    elif len(args) > 1:
        parser.print_usage(stderr)
        print >> stderr, parser.get_prog_name() + ': error:', \
                         'too many arguments'
        return 2
    for filename in args:
        try:
            css = compile(
                filename=filename,
                output_style=options.output_style,
                include_paths=options.include_paths,
                image_path=options.image_path
            )
        except CompileError as e:
            print >> stderr, parser.get_prog_name() + ': error:', e
            return 1
        else:
            print css
    return 0


if __name__ == '__main__':
    sys.exit(main())
