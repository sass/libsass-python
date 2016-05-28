Contributor's guide
===================

Coding style
------------

- Follow `PEP 8`_.  flake8_ would help.
- Order imports by lexicographical order.
- Prefer relative imports.
- All functions, classes, methods, attributes, and modules should have
  the docstring.
- Functions and methods should contain ``:param:``, ``:type:``
  (``:return:``, ``:rtype`` if it returns something),
  (``:raise:`` if it may raise an error) in their docstring.

.. _flake8: https://gitlab.com/pycqa/flake8
.. _PEP 8: www.python.org/dev/peps/pep-0008


Tests
-----

- All code patches should contain one or more unit tests or regression tests.
- All code patches have to successfully run tests on every Python version
  we aim to support.  tox_ would help.
- All commits will be tested by Travis_ (Linux) and
  AppVeyor_ (Windows).

.. _tox:  http://tox.testrun.org/
.. _Travis: http://travis-ci.org/dahlia/libsass-python
.. _AppVeyor: https://ci.appveyor.com/project/dahlia/libsass-python


Maintainer's guide
==================

Releasing
---------

Here's a brief check list for releasing a new version:

- Double check if the version is correctly bumped.
  You can bump the version by changing ``__version__`` in sass.py file.
  Note that it might be already bumped by other maintainers,
  so check what's the latest release version from PyPI_.
- The changelog has to be complete, and frozen.
  "To be released" sentence has to be replaced by the actual release date.
- If the code freeze for the release is done (including version bump),
  tag the commit using ``git tag`` command.  The tag name has to simply be
  the version name e.g. ``1.2.3``.  Of course, the tag also has to be pushed
  to the upstream repository.
- Make a source distribution and upload it to PyPI
  (``python3 setup.py sdist upload``).
  If it's successful the new version must appear on PyPI_.
- AppVeyor_ automatically makes binary wheels for Windows, but each CI build
  takes longer than an hour.  These wheels are not automatically uploaded,
  but there's upload_appveyor_builds.py script that downloads built wheels and
  uploads them to PyPI.
- Run build_manylinux_wheels.py to build linux wheels and upload them to
  PyPI (takes ~10 minutes).
- The `docs website`__ also has to be updated.
  It's currently a static website deployed on GitHub Pages.
  Use ``python setup.py upload_doc`` command.
  Although it seems possible to be automated using Travis.
- Manually create a release through https://github.com/dahlia/libsass-python/releases/

Ping Hong Minhee (hongminhee@member.fsf.org, @dahlia on GitHub) if you need
any help!

.. _PyPI: https://pypi.python.org/pypi/libsass
__ http://hongminhee.org/libsass-python/
