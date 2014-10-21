from __future__ import print_function, with_statement

import ast
import distutils.cmd
import distutils.log
import glob
import os
import os.path
import platform
import re
import shutil
import sys
import tempfile
import time

try:
    from setuptools import Extension, setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import Extension, setup

LIBSASS_DIR = 'libsass'

MAKEFILE_SOURCES_LIST_RE = re.compile(r'''
    (?: ^ | \n ) (?: libsass_la_ )? SOURCES [ \t]* = [ \t]*
    (?P<sources> (?: (?: $ | [ \t] | \\ [\n] )+
                     [^ \n\t\\]+ )+ )
''', re.VERBOSE)


if not os.path.isfile(os.path.join(LIBSASS_DIR, 'Makefile')) and \
   os.path.isdir('.git'):
    print(file=sys.stderr)
    print('You seem to miss initializing submodules; '
          'try the following command', file=sys.stderr)
    print('  git submodule update --init', file=sys.stderr)
    print(file=sys.stderr)

libsass_sources = set()
for makefilename in [
        os.path.join(LIBSASS_DIR, 'Makefile'),
        os.path.join(LIBSASS_DIR, 'Makefile.am')]:
    with open(makefilename) as makefile:
        sources_match = MAKEFILE_SOURCES_LIST_RE.search(makefile.read())
        sources_list = sources_match.group('sources').replace('\\\n', ' ')
        libsass_sources.update(sources_list.split())
libsass_sources = list(libsass_sources)

libsass_headers = [
    os.path.join(LIBSASS_DIR, 'sass_interface.h'),
    os.path.join(LIBSASS_DIR, 'sass.h'),
    os.path.join(LIBSASS_DIR, 'win32', 'unistd.h'),
]
libsass_headers.extend(glob.glob('*.hpp'))
include_dirs = ['utf8']
sources = ['pysass.cpp']
sources.extend([os.path.join(LIBSASS_DIR, s) for s in libsass_sources])

if sys.platform == 'win32':
    from distutils.msvc9compiler import get_build_version
    vscomntools_env = 'VS{0}{1}COMNTOOLS'.format(
        int(get_build_version()),
        int(get_build_version() * 10) % 10
    )
    try:
        os.environ[vscomntools_env] = os.environ['VS120COMNTOOLS']
    except KeyError:
        distutils.log.warn('You probably need Visual Studio 2013 (12.0) '
                           'or higher')
    from distutils import msvccompiler, msvc9compiler
    if msvccompiler.get_build_version() < 12.0:
        msvccompiler.get_build_version = lambda: 12.0
    if get_build_version() < 12.0:
        msvc9compiler.get_build_version = lambda: 12.0
        msvc9compiler.VERSION = 12.0
    # Workaround http://bugs.python.org/issue4431 under Python <= 2.6
    if sys.version_info < (2, 7):
        def spawn(self, cmd):
            from distutils.spawn import spawn
            if cmd[0] == self.linker:
                for i, val in enumerate(cmd):
                    if val.startswith('/MANIFESTFILE:'):
                        spawn(cmd[:i] + ['/MANIFEST'] + cmd[i:],
                              dry_run=self.dry_run)
                        return
            spawn(cmd, dry_run=self.dry_run)
        from distutils.msvc9compiler import MSVCCompiler
        MSVCCompiler.spawn = spawn
    flags = ['-I' + os.path.abspath('win32')]
    link_flags = []
else:
    flags = ['-fPIC', '-std=c++11', '-Wall', '-Wno-parentheses']
    platform.mac_ver()
    if platform.system() == 'Darwin':
        flags.extend([
            '-stdlib=libc++',
            '-mmacosx-version-min=10.7',
        ])
        if tuple(map(int, platform.mac_ver()[0].split('.'))) >= (10, 9):
            flags.append(
                '-Wno-error=unused-command-line-argument-hard-error-in-future',
            )
    link_flags = ['-fPIC', '-lstdc++']

sass_extension = Extension(
    '_sass',
    sources,
    library_dirs=[os.path.join('.', LIBSASS_DIR)],
    include_dirs=[os.path.join('.', LIBSASS_DIR)],
    depends=libsass_headers,
    extra_compile_args=['-c', '-O2'] + flags,
    extra_link_args=link_flags,
    language='c++',
)


def version(sass_filename='sass.py'):
    with open(sass_filename) as f:
        tree = ast.parse(f.read(), sass_filename)
    for node in tree.body:
        if isinstance(node, ast.Assign) and \
           len(node.targets) == 1:
            target, = node.targets
            if isinstance(target, ast.Name) and target.id == '__version__':
                return node.value.s


def get_unstable_commit():
    try:
        with open('.unstable-release') as f:
            return f.read().strip() or None
    except (IOError, OSError):
        return


unstable_commit = get_unstable_commit()


def readme():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
            return f.read()
    except IOError:
        pass


class upload_doc(distutils.cmd.Command):
    """Uploads the documentation to GitHub pages."""

    description = __doc__
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        path = tempfile.mkdtemp()
        build = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'build', 'sphinx', 'html')
        os.chdir(path)
        os.system('git clone -b gh-pages --depth 5 '
                  'git@github.com:dahlia/libsass-python.git .')
        os.system('git rm -r .')
        os.system('touch .nojekyll')
        os.system('cp -r ' + build + '/* .')
        os.system('git stage .')
        os.system('git commit -a -m "Documentation updated."')
        os.system('git push origin gh-pages')
        shutil.rmtree(path)


setup(
    name='libsass' + ('-unstable' if unstable_commit else ''),
    description='SASS for Python: '
                'A straightforward binding of libsass for Python.',
    long_description=readme(),
    version=version() + (time.strftime('.%Y%m%d.') + unstable_commit
                         if unstable_commit else ''),
    ext_modules=[sass_extension],
    packages=['sassutils'],
    py_modules=['sass', 'sassc', 'sasstests'],
    package_data={
        '': [
            'README.rst',
            os.path.join(LIBSASS_DIR, 'Makefile'),
            os.path.join(LIBSASS_DIR, 'Makefile.am'),
            'win32/*.h', 'test/*.sass'
        ]
    },
    scripts=['sassc.py'],
    license='MIT License',
    author='Hong Minhee',
    author_email='minhee' '@' 'dahlia.kr',
    url='http://hongminhee.org/libsass-python/',
    download_url='https://github.com/dahlia/libsass-python/releases',
    entry_points={
        'distutils.commands': [
            'build_sass = sassutils.distutils:build_sass'
        ],
        'distutils.setup_keywords': [
            'sass_manifests = sassutils.distutils:validate_manifests'
        ],
        'console_scripts': [
            ['sassc = sassc:main']
        ]
    },
    install_requires=['six'],
    tests_require=['Werkzeug >= 0.9'],
    test_suite='sasstests.suite',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: C',
        'Programming Language :: C++',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Compilers'
    ],
    cmdclass={'upload_doc': upload_doc}
)
