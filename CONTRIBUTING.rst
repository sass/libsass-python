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
.. _PEP 8: https://www.python.org/dev/peps/pep-0008


Tests
-----

- All code patches should contain one or more unit tests or regression tests.
- All code patches have to successfully run tests on every Python version
  we aim to support.  tox_ would help.
- All commits will be tested by `Azure Pipelines`_ (Linux and Windows).

.. _tox:  https://tox.readthedocs.io/
.. _`Azure Pipelines`: https://dev.azure.com/asottile/asottile/_build/latest?definitionId=22&branchName=main


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
- `Azure Pipelines`_ automatically makes binary wheels for Windows, but each
  CI build takes a while.  These wheels are not automatically uploaded,
  but there's ``./bin/download-windows-wheels`` script that downloads built
  wheels.  Then upload them with ``twine``.
- Run ``./bin/build-manylinux-wheels`` to build linux wheels and upload them to
  PyPI (takes ~5 minutes).
- The `docs website`__ also has to be updated.
  It's currently a static website deployed on GitHub Pages.
  Use ``python setup.py upload_doc`` command.
  Although it seems possible to be automated using Github Actions.
- Manually create a release through https://github.com/sass/libsass-python/releases/

Ping Hong Minhee (hongminhee@member.fsf.org, @dahlia on GitHub) if you need
any help!

.. _PyPI: https://pypi.org/pypi/libsass/
__ https://sass.github.io/libsass-python/
