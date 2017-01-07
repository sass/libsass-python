#!/usr/bin/env python3.5
"""Script for building 'manylinux' wheels for libsass.

Run me after putting the source distribution on pypi.

See: https://www.python.org/dev/peps/pep-0513/
"""
import os
import pipes
import subprocess
import tempfile

from twine.commands import upload


def check_call(*cmd):
    print(
        'build-manylinux-wheels>> ' +
        ' '.join(pipes.quote(part) for part in cmd),
    )
    subprocess.check_call(cmd)


def main():
    os.makedirs('dist', exist_ok=True)
    for python in (
            'cp27-cp27mu',
            'cp34-cp34m',
            'cp35-cp35m',
            'cp36-cp36m',
    ):
        with tempfile.TemporaryDirectory() as work:
            pip = '/opt/python/{}/bin/pip'.format(python)
            check_call(
                'docker', 'run', '-ti',
                # Use this so the files are not owned by root
                '--user', '{}:{}'.format(os.getuid(), os.getgid()),
                # We'll do building in /work and copy results to /dist
                '-v', '{}:/work:rw'.format(work),
                '-v', '{}:/dist:rw'.format(os.path.abspath('dist')),
                'quay.io/pypa/manylinux1_x86_64:latest',
                'bash', '-exc',
                '{} wheel --verbose --wheel-dir /work --no-deps libsass && '
                'auditwheel repair --wheel-dir /dist /work/*.whl'.format(pip)
            )
    dists = tuple(os.path.join('dist', p) for p in os.listdir('dist'))
    return upload.main(('-r', 'pypi') + dists)


if __name__ == '__main__':
    exit(main())
