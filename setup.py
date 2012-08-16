try:
    from setuptools import Extension, setup
except ImportError:
    from distutils.core import Extension, setup


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
    depends=libsass_headers,
    extra_compile_args=['-c', '-Wall', '-O2', '-fPIC'],
    extra_link_args=['-fPIC'],
)

setup(
    name='libsass',
    version='0.1.0',
    ext_modules=[sass_extension],
    py_modules=['sasstests'],
    license='MIT License',
    author='Hong Minhee',
    author_email='minhee' '@' 'dahlia.kr',
    url='https://github.com/dahlia/libsass-python',
    tests_require=['Attest'],
    test_loader='attest:auto_reporter.test_loader',
    test_suite='sasstests.suite'
)
