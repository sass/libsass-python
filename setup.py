from __future__ import with_statement

import os.path

try:
    from setuptools import Extension, setup
except ImportError:
    from distutils.core import Extension, setup


version = '0.1.0'

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
    'sass_interface.h'
]

sass_extension = Extension(
    'sass',
    ['sass.c'] + libsass_sources,
    define_macros=[('LIBSASS_PYTHON_VERSION', '"' + version + '"')],
    depends=libsass_headers,
    extra_compile_args=['-c', '-O2', '-fPIC',
                        '-Wall', '-Wno-parentheses',
                        '-Wno-tautological-compare'],
    extra_link_args=['-fPIC'],
)


def readme():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
            return f.read()
    except IOError:
        pass

setup(
    name='libsass',
    description='SASS for Python: '
                'A straightforward binding of libsass for Python.',
    long_description=readme(),
    version=version,
    ext_modules=[sass_extension],
    py_modules=['sasstests'],
    package_data={'': ['README.rst', 'test/*.sass']},
    license='MIT License',
    author='Hong Minhee',
    author_email='minhee' '@' 'dahlia.kr',
    url='https://github.com/dahlia/libsass-python',
    tests_require=['Attest'],
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
    ]
)
