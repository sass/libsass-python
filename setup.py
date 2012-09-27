from __future__ import with_statement

import distutils.cmd
import os
import os.path
import shutil
import sys
import tempfile
import warnings

try:
    from setuptools import Extension, setup
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import Extension, setup


version = '0.2.2'

libsass_sources = [ 
    'context.cpp', 'functions.cpp', 'document.cpp',
    'document_parser.cpp', 'eval_apply.cpp', 'node.cpp',
    'node_factory.cpp', 'node_emitters.cpp', 'prelexer.cpp',
    'sass_interface.cpp',
]

libsass_headers = [
    'color_names.hpp', 'error.hpp', 'node.hpp',
    'context.hpp', 'eval_apply.hpp', 'node_factory.hpp',
    'document.hpp', 'functions.hpp', 'prelexer.hpp',
    'sass_interface.h', 'win32/unistd.h'
]

if sys.platform == 'win32':
    try:
        os.environ['VS90COMNTOOLS'] = os.environ['VS110COMNTOOLS']
    except KeyError:
        warnings.warn('You probably need Visual Studio 2012 (11.0) or higher')
    # Workaround http://bugs.python.org/issue4431 under Python <= 2.6
    if sys.version < (2, 7):
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
    macros = {'LIBSASS_PYTHON_VERSION': '\\"' + version + '\\"'}
else:
    flags = ['-fPIC', '-Wall', '-Wno-parentheses', '-Wno-tautological-compare']
    link_flags = ['-fPIC', '-lstdc++']
    macros = {'LIBSASS_PYTHON_VERSION': '"' + version + '"'}

sass_extension = Extension(
    'sass',
    ['sass.c'] + libsass_sources,
    define_macros=macros.items(),
    depends=libsass_headers,
    extra_compile_args=['-c', '-O2'] + flags,
    extra_link_args=link_flags,
)


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
        os.system('git clone git@github.com:dahlia/libsass-python.git .')
        os.system('git checkout gh-pages')
        os.system('git rm -r .')
        os.system('touch .nojekyll')
        os.system('cp -r ' + build + '/* .')
        os.system('git stage .')
        os.system('git commit -a -m "Documentation updated."')
        os.system('git push origin gh-pages')
        shutil.rmtree(path)


setup(
    name='libsass',
    description='SASS for Python: '
                'A straightforward binding of libsass for Python.',
    long_description=readme(),
    version=version,
    ext_modules=[sass_extension],
    packages=['sassutils'],
    py_modules=['sasstests'],
    package_data={'': ['README.rst', 'test/*.sass']},
    license='MIT License',
    author='Hong Minhee',
    author_email='minhee' '@' 'dahlia.kr',
    url='http://dahlia.kr/libsass-python/',
    entry_points={
        'distutils.commands': [
            'build_sass = sassutils.distutils:build_sass'
        ],
        'distutils.setup_keywords': [
            'sass_manifests = sassutils.distutils:validate_manifests'
        ]
    },
    tests_require=['Attest', 'Werkzeug'],
    test_loader='attest:auto_reporter.test_loader',
    test_suite='sasstests.suite',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: C',
        'Programming Language :: C++',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Compilers'
    ],
    cmdclass={'upload_doc': upload_doc}
)
