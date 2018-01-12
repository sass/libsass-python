Using with Flask
================

This guide explains how to use libsass with Flask_ web framework.
:mod:`sassutils` package provides several tools that can be integrated
to web applications written in Flask.

.. _Flask: http://flask.pocoo.org/

.. contents::


Directory layout
----------------

Imagine the project contained in such directory layout:

- :file:`setup.py`
- :file:`myapp/`

  - :file:`__init__.py`
  - :file:`static/`

    - :file:`sass/`
    - :file:`css/`
  - :file:`templates/`

SASS/SCSS files will go inside :file:`myapp/static/sass/` directory.
Compiled CSS files will go inside :file:`myapp/static/css/` directory.
CSS files can be regenerated, so add :file:`myapp/static/css/` into your
ignore list like :file:`.gitignore` or :file:`.hgignore`.


Defining manifest
-----------------

The :mod:`sassutils` defines a concept named :dfn:`manifest`.
Manifest is building settings of SASS/SCSS.  It specifies some paths
related to building SASS/SCSS:

- The path of the directory which contains SASS/SCSS source files.
- The path of the directory compiled CSS files will go.
- The path, is exposed to HTTP (through WSGI), of the directory that
  will contain compiled CSS files.

Every package may have their own manifest.  Paths have to be relative
to the path of the package.

For example, in the project the package name is :mod:`myapp`.
The path of the package is :file:`myapp/`.  The path of SASS/SCSS directory
is :file:`static/sass/` (relative to the package directory).
The path of CSS directory is :file:`static/css/`.
The exposed path is :file:`/static/css`.

This settings can be represented as the following manifests::

    {
        'myapp': ('static/sass', 'static/css', '/static/css')
    }

As you can see the above, the set of manifests are represented in dictionary.
Keys are packages names.  Values are tuples of paths.


Building SASS/SCSS for each request
-----------------------------------

.. seealso::

   Flask --- `Hooking in WSGI Middlewares`__
      The section which explains how to integrate WSGI middlewares to
      Flask.

   Flask --- :ref:`flask:app-dispatch`
      The documentation which explains how Flask dispatch each
      request internally.

   __ http://flask.pocoo.org/docs/quickstart/#hooking-in-wsgi-middlewares

In development, to manually build SASS/SCSS files for each change is
so tiring.  :class:`~sassutils.wsgi.SassMiddleware` makes the web
application to automatically build SASS/SCSS files for each request.
It's a WSGI middleware, so it can be plugged into the web app written in
Flask.

:class:`~sassutils.wsgi.SassMiddleware` takes two required parameters:

- The WSGI-compliant callable object.
- The set of manifests represented as dictionary.

So::

    from flask import Flask
    from sassutils.wsgi import SassMiddleware

    app = Flask(__name__)

    app.wsgi_app = SassMiddleware(app.wsgi_app, {
        'myapp': ('static/sass', 'static/css', '/static/css')
    })

And then, if you want to link a compiled CSS file, use :func:`~flask.url_for()`
function:

.. sourcecode:: html+jinja

   <link href="{{ url_for('static', filename='css/style.scss.css') }}"
         rel="stylesheet" type="text/css">

.. note::

   The linked filename is :file:`style.scss.css`, not just :file:`style.scss`.
   All compiled filenames have trailing ``.css`` suffix.


Building SASS/SCSS for each deployment
--------------------------------------

.. note::

   This section assumes that you use setuptools_ for deployment.

.. seealso::

   Flask --- :ref:`flask:distribute-deployment`
      How to deploy Flask application using setuptools_.

If libsass has been installed in the :file:`site-packages` (for example,
your virtualenv), :file:`setup.py` script also gets had new command
provided by libsass: :class:`~sassutils.distutils.build_sass`.
The command is aware of ``sass_manifests`` option of :file:`setup.py` and
builds all SASS/SCSS sources according to the manifests.

Add these arguments to :file:`setup.py` script::

    setup(
        # ...,
        setup_requires=['libsass >= 0.6.0'],
        sass_manifests={
            'myapp': ('static/sass', 'static/css', '/static/css')
        }
    )

The ``setup_requires`` option makes sure that the libsass is installed
in :file:`site-packages` (for example, your virtualenv) before
:file:`setup.py` script.  That means: if you run :file:`setup.py` script
and libsass isn't installed yet at the moment, it will automatically
install libsass first.

The ``sass_manifests`` specifies the manifests for libsass.

Now :program:`setup.py build_sass` will compile all SASS/SCSS files
in the specified path and generates compiled CSS files into the specified
path (according to the manifests).

If you use it with ``sdist`` or ``bdist`` command, a packed archive also
will contain compiled CSS files!

.. sourcecode:: console

   $ python setup.py build_sass sdist

You can add aliases to make these commands to always run ``build_sass``
command before.  Make :file:`setup.cfg` config:

.. sourcecode:: ini

   [aliases]
   sdist = build_sass sdist
   bdist = build_sass bdist

Now it automatically builds SASS/SCSS sources and include compiled CSS files
to the package archive when you run :program:`setup.py sdist`.

.. _setuptools: https://pypi.python.org/pypi/setuptools
