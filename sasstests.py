from __future__ import with_statement
from attest import assert_hook

import re

from attest import Tests, raises

import sass


suite = Tests()


@suite.test
def version():
    assert re.match(r'^\d+\.\d+\.\d+$', sass.__version__)


@suite.test
def compile_required_arguments():
    with raises(TypeError):
        sass.compile()


@suite.test
def compile_takes_only_keywords():
    with raises(TypeError):
        sass.compile('a { color: blue; }')


@suite.test
def compile_exclusive_arguments():
    with raises(TypeError):
        sass.compile(string='a { color: blue; }',
                     filename='test/a.sass')
    with raises(TypeError):
        sass.compile(string='a { color: blue; }',
                     dirname='test/')
    with raises(TypeError):
        sass.compile(filename='test/a.sass',
                     dirname='test/')


@suite.test
def compile_invalid_output_style():
    with raises(TypeError):
        sass.compile(string='a { color: blue; }', output_style=['compact'])
    with raises(TypeError):
        sass.compile(string='a { color: blue; }', output_style=123j)
    with raises(ValueError):
        sass.compile(string='a { color: blue; }', output_style='invalid')


@suite.test
def compile_invalid_image_path():
    with raises(TypeError):
        sass.compile(string='a { color: blue; }', image_path=[])
    with raises(TypeError):
        sass.compile(string='a { color: blue; }', image_path=123)


@suite.test
def compile_string():
    actual = sass.compile(string='a { b { color: blue; } }')
    assert actual == 'a b {\n  color: blue; }\n'
    with raises(sass.CompileError):
        sass.compile(string='a { b { color: blue; }')
    # sass.CompileError should be a subtype of ValueError
    with raises(ValueError):
        sass.compile(string='a { b { color: blue; }')
    with raises(TypeError):
        sass.compile(string=1234)
    with raises(TypeError):
        sass.compile(string=[])


@suite.test
def compile_filename():
    actual = sass.compile(filename='test/a.sass')
    assert actual == '''\
body {
  background-color: green; }
  body a {
    color: blue; }
'''
    with raises(TypeError):
        sass.compile(filename=1234)
    with raises(TypeError):
        sass.compile(filename=[])
