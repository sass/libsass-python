Using with Flask
================

This guide explains how to use libsass with the Flask_ web framework.
:mod:`sassutils` package provides several tools that can be integrated
into web applications written in Flask.

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

Sass/SCSS files will go inside :file:`myapp/static/sass/` directory.
Compiled CSS files will go inside :file:`myapp/static/css/` directory.
CSS files can be regenerated, so add :file:`myapp/static/css/` into your
ignore list like :file:`.gitignore` or :file:`.hgignore`.


Defining manifest
-----------------

The :mod:`sassutils` defines a concept named :dfn:`manifest`.
Manifest is the build settings of Sass/SCSS.  It specifies some paths
related to building Sass/SCSS:

- The path of the directory which contains Sass/SCSS source files.
- The path of the directory which the compiled CSS files will go.
- The path, exposed to HTTP (through WSGI), of the directory that
  will contain the compiled CSS files.

Every package may have its own manifest.  Paths have to be relative
to the path of the package.

For example, in the above project, the package name is :mod:`myapp`.
The path of the package is :file:`myapp/`.  The path of the Sass/SCSS
directory is :file:`static/sass/` (relative to the package directory).
The path of the CSS directory is :file:`static/css/`.
The exposed path is :file:`/static/css`.

These settings can be represented as the following manifests::

    {
        'myapp': ('static/sass', 'static/css', '/static/css')
    }

As you can see the above, the set of manifests are represented in dictionary,
in which the keys are packages names and the values are tuples of paths.


Building Sass/SCSS for each request
-----------------------------------

.. seealso::

   Flask --- `Hooking in WSGI Middlewares`__
      The section which explains how to integrate WSGI middlewares to
      Flask.

   Flask --- :ref:`flask:app-dispatch`
      The documentation which explains how Flask dispatches each
      request internally.

   __ http://flask.pocoo.org/docs/quickstart/#hooking-in-wsgi-middlewares

In development, manually building Sass/SCSS files for each change is
a tedious task.  :class:`~sassutils.wsgi.SassMiddleware` makes the web
application build Sass/SCSS files for each request automatically.
It's a WSGI middleware, so it can be plugged into the web app written in
Flask.

:class:`~sassutils.wsgi.SassMiddleware` takes two required parameters:

- The WSGI-compliant callable object.
- The set of manifests represented as a dictionary.

So::

    from flask import Flask
    from sassutils.wsgi import SassMiddleware

    app = Flask(__name__)

    app.wsgi_app = SassMiddleware(app.wsgi_app, {
        'myapp': ('static/sass', 'static/css', '/static/css')
    })

And then, if you want to link a compiled CSS file, use the
:func:`~flask.url_for()` function:

.. sourcecode:: html+jinja

   <link href="{{ url_for('static', filename='css/style.scss.css') }}"
         rel="stylesheet" type="text/css">

.. note::

   The linked filename is :file:`style.scss.css`, not just :file:`style.scss`.
   All compiled filenames have trailing ``.css`` suffix.


Building Sass/SCSS for each deployment
--------------------------------------

.. note::

   This section assumes that you use setuptools_ for deployment.

.. seealso::

   Flask --- :ref:`flask:distribute-deployment`
      How to deploy Flask application using setuptools_.

If libsass is installed in the :file:`site-packages` (for example,
your virtualenv), the :file:`setup.py` script also gets a new command
provided by libsass: :class:`~sassutils.distutils.build_sass`.
The command is aware of the ``sass_manifests`` option of :file:`setup.py` and
builds all Sass/SCSS sources according to the manifests.

Add these arguments to :file:`setup.py` script::

    setup(
        # ...,
        setup_requires=['libsass >= 0.6.0'],
        sass_manifests={
            'myapp': ('static/sass', 'static/css', '/static/css')
        }
    )

The ``setup_requires`` option makes sure that libsass is installed
in :file:`site-packages` (for example, your virtualenv) before
the :file:`setup.py` script.  That means if you run the :file:`setup.py`
script and libsass isn't installed in advance, it will automatically
install libsass first.

The ``sass_manifests`` specifies the manifests for libsass.

Now :program:`setup.py build_sass` will compile all Sass/SCSS files
in the specified path and generates compiled CSS files inside the specified
path (according to the manifests).

If you use it with ``sdist`` or ``bdist`` commands, the packed archive will
also contain the compiled CSS files!

.. sourcecode:: console

   $ python setup.py build_sass sdist

You can add aliases to make these commands always run the ``build_sass``
command first.  Make :file:`setup.cfg` config:

.. sourcecode:: ini

   [aliases]
   sdist = build_sass sdist
   bdist = build_sass bdist

Now it automatically builds Sass/SCSS sources and include the compiled CSS files
to the package archive when you run :program:`setup.py sdist`.

.. _setuptools: https://pypi.org/pypi/setuptools/
