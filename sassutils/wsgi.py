""":mod:`sassutils.wsgi` --- WSGI middleware for development purpose
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from __future__ import absolute_import, with_statement

import os
import os.path

import pkg_resources

from sass import CompileError
from .builder import Manifest
from .utils import is_mapping

__all__ = 'SassMiddleware',


class SassMiddleware(object):
    """WSGI middleware for development purpose.  Everytime a CSS file has
    requested it finds a matched SASS/SCSS source file and then compiled
    it into CSS.

    :param app: the WSGI application to wrap
    :type app: :class:`collections.Callable`
    :param manifests: build settings.  the same format to
                      :file:`setup.py` script's ``sass_manifests``
                      option
    :type manifests: :class:`collections.Mapping`
    :param package_dir: optional mapping of package names to directories.
                        the same format to :file:`setup.py` script's
                        ``package_dir`` option
    :type package_dir: :class:`collections.Mapping`

    """

    def __init__(self, app, manifests, package_dir={},
                 error_status='500 Internal Server Error'):
        if not callable(app):
            raise TypeError('app must be a WSGI-compliant callable object, '
                            'not ' + repr(app))
        self.app = app
        self.manifests = Manifest.normalize_manifests(manifests)
        if not is_mapping(package_dir):
            raise TypeError('package_dir must be a mapping object, not ' +
                            repr(package_dir))
        self.error_status = error_status
        self.package_dir = dict(package_dir)
        for package_name in self.manifests:
            if package_name in self.package_dir:
                continue
            path = pkg_resources.resource_filename(package_name, '')
            self.package_dir[package_name] = path
        self.paths = []
        for package_name, manifest in self.manifests.iteritems():
            wsgi_path = manifest.wsgi_path
            if not wsgi_path.startswith('/'):
                wsgi_path = '/' + wsgi_path
            if not wsgi_path.endswith('/'):
                wsgi_path += '/'
            package_dir = self.package_dir[package_name]
            self.paths.append((wsgi_path, package_dir, manifest))

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '/')
        if path.endswith('.css'):
            for prefix, package_dir, manifest in self.paths:
                if not path.startswith(prefix):
                    continue
                css_filename = path[len(prefix):]
                sass_filename = css_filename[:-4]
                try:
                    result = manifest.build_one(package_dir, sass_filename)
                except (IOError, OSError):
                    break
                except CompileError, e:
                    start_response(self.error_status,
                                   [('Content-Type', 'text/css')])
                    return [
                        '/*\n', str(e), '\n*/\n\n',
                        'body:before { content: ',
                        self.quote_css_string(str(e)),
                        '; color: maroon; background-color: white; }'
                    ]
                out = start_response('200 OK', [('Content-Type', 'text/css')])
                with open(os.path.join(package_dir, result), 'r') as in_:
                    while 1:
                        chunk = in_.read(4096)
                        if chunk:
                            out(chunk)
                        else:
                            break
                return ()
        return self.app(environ, start_response)

    @staticmethod
    def quote_css_string(s):
        """Quotes a string as CSS string literal."""
        return "'" + ''.join('\\%06x' % ord(c) for c in s) + "'"
