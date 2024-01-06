import atexit
import os.path
import platform
import shutil
import subprocess
import sys
import tempfile

import distutils.cmd
import distutils.log
import distutils.sysconfig
from setuptools import Extension
from setuptools import setup

MACOS_FLAG = ['-mmacosx-version-min=10.7']
FLAGS_POSIX = [
    '-fPIC', '-std=gnu++0x', '-Wall', '-Wno-parentheses', '-Werror=switch',
]
FLAGS_CLANG = ['-c', '-O3'] + FLAGS_POSIX + ['-stdlib=libc++']
LFLAGS_POSIX = ['-fPIC',  '-lstdc++']
LFLAGS_CLANG = ['-fPIC', '-stdlib=libc++']

sources = ['_sass.c']
headers = []

if sys.platform == 'win32':
    extra_compile_args = ['/Od', '/EHsc', '/MT']
    extra_link_args = []
elif platform.system() == 'Darwin':
    extra_compile_args = FLAGS_CLANG + MACOS_FLAG
    extra_link_args = LFLAGS_CLANG + MACOS_FLAG
elif platform.system() in {'FreeBSD', 'OpenBSD'}:
    extra_compile_args = FLAGS_CLANG
    extra_link_args = LFLAGS_CLANG
else:
    extra_compile_args = FLAGS_POSIX
    extra_link_args = LFLAGS_POSIX

if platform.system() in {'Darwin', 'FreeBSD', 'OpenBSD'}:
    os.environ.setdefault('CC', 'clang')
    os.environ.setdefault('CXX', 'clang++')
    orig_customize_compiler = distutils.sysconfig.customize_compiler

    def customize_compiler(compiler):
        orig_customize_compiler(compiler)
        compiler.compiler[0] = os.environ['CC']
        compiler.compiler_so[0] = os.environ['CXX']
        compiler.compiler_cxx[0] = os.environ['CXX']
        compiler.linker_so[0] = os.environ['CXX']
        return compiler
    distutils.sysconfig.customize_compiler = customize_compiler

if os.environ.get('SYSTEM_SASS', False):
    libraries = ['sass']
    include_dirs = []
else:
    LIBSASS_SOURCE_DIR = os.path.join('libsass', 'src')

    if (
            not os.path.isfile(os.path.join('libsass', 'Makefile')) and
            os.path.isdir('.git')
    ):
        print(file=sys.stderr)
        print('Missing the libsass sumbodule.  Try:', file=sys.stderr)
        print('  git submodule update --init', file=sys.stderr)
        print(file=sys.stderr)
        exit(1)

    # Determine the libsass version from the git checkout
    if os.path.exists(os.path.join('libsass', '.git')):
        out = subprocess.check_output((
            'git', '-C', 'libsass', 'describe',
            '--abbrev=4', '--dirty', '--always', '--tags',
        ))
        with open('.libsass-upstream-version', 'wb') as libsass_version_file:
            libsass_version_file.write(out)

    # The version file should always exist at this point
    with open('.libsass-upstream-version', 'rb') as libsass_version_file:
        libsass_version = libsass_version_file.read().decode('UTF-8').strip()
        if sys.platform == 'win32':
            # This looks wrong, but is required for some reason :(
            define = fr'/DLIBSASS_VERSION="\"{libsass_version}\""'
        else:
            define = f'-DLIBSASS_VERSION="{libsass_version}"'

    for directory in (
            os.path.join('libsass', 'src'),
            os.path.join('libsass', 'include'),
    ):
        for pth, _, filenames in os.walk(directory):
            for filename in filenames:
                filename = os.path.join(pth, filename)
                if filename.endswith(('.c', '.cpp')):
                    sources.append(filename)
                elif filename.endswith('.h'):
                    headers.append(filename)

    if sys.platform == 'win32':
        from distutils.msvc9compiler import get_build_version
        vscomntools_env = 'VS{}{}COMNTOOLS'.format(
            int(get_build_version()),
            int(get_build_version() * 10) % 10,
        )
        try:
            os.environ[vscomntools_env] = os.environ['VS140COMNTOOLS']
        except KeyError:
            distutils.log.warn(
                'You probably need Visual Studio 2015 (14.0) '
                'or higher',
            )
        from distutils import msvccompiler, msvc9compiler
        if msvccompiler.get_build_version() < 14.0:
            msvccompiler.get_build_version = lambda: 14.0
        if get_build_version() < 14.0:
            msvc9compiler.get_build_version = lambda: 14.0
            msvc9compiler.VERSION = 14.0
    elif platform.system() in {'Darwin', 'FreeBSD', 'OpenBSD'}:
        # Dirty workaround to avoid link error...
        # Python distutils doesn't provide any way
        # to configure different flags for each cc and c++.
        cencode_path = os.path.join(LIBSASS_SOURCE_DIR, 'cencode.c')
        cencode_body = ''
        with open(cencode_path) as f:
            cencode_body = f.read()
        with open(cencode_path, 'w') as f:
            f.write(
                '#ifdef __cplusplus\n'
                'extern "C" {\n'
                '#endif\n',
            )
            f.write(cencode_body)
            f.write(
                '#ifdef __cplusplus\n'
                '}\n'
                '#endif\n',
            )

        @atexit.register
        def restore_cencode():
            if os.path.isfile(cencode_path):
                with open(cencode_path, 'w') as f:
                    f.write(cencode_body)

    libraries = []
    include_dirs = [os.path.join('.', 'libsass', 'include')]
    extra_compile_args.append(define)

# Py_LIMITED_API does not work for pypy
# https://foss.heptapod.net/pypy/pypy/issues/3173
if not hasattr(sys, 'pypy_version_info'):
    py_limited_api = True
    define_macros = [('Py_LIMITED_API', None)]
else:
    py_limited_api = False
    define_macros = []

sass_extension = Extension(
    '_sass',
    sorted(sources),
    include_dirs=include_dirs,
    depends=headers,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    libraries=libraries,
    py_limited_api=py_limited_api,
    define_macros=define_macros,
)


class upload_doc(distutils.cmd.Command):
    """Uploads the documentation to GitHub pages."""

    description = __doc__
    user_options = []

    def initialize_options(self):
        if sys.version_info < (3,):
            raise SystemExit('upload_doc must be run with python 3')

    def finalize_options(self):
        pass

    def run(self):
        path = tempfile.mkdtemp()
        build = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'build', 'sphinx', 'html',
        )
        os.chdir(path)
        os.system(
            'git clone -b gh-pages --depth 5 '
            'git@github.com:sass/libsass-python.git .',
        )
        os.system('git rm -r .')
        os.system('touch .nojekyll')
        os.system('cp -r ' + build + '/* .')
        os.system('git stage .')
        os.system('git commit -a -m "Documentation updated."')
        os.system('git push origin gh-pages')
        shutil.rmtree(path)


cmdclass = {'upload_doc': upload_doc}

if sys.version_info >= (3,) and platform.python_implementation() == 'CPython':
    try:
        import wheel.bdist_wheel
    except ImportError:
        pass
    else:
        class bdist_wheel(wheel.bdist_wheel.bdist_wheel):
            def finalize_options(self):
                self.py_limited_api = f'cp3{sys.version_info[1]}'
                super().finalize_options()

        cmdclass['bdist_wheel'] = bdist_wheel


setup(
    ext_modules=[sass_extension],
    cmdclass=cmdclass,
)
