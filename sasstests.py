from __future__ import with_statement
from attest import assert_hook

import os.path
import re
import shutil
import tempfile

from attest import Tests, raises

import sass
from sassutils.builder import build_directory


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


A_EXPECTED_CSS = '''\
body {
  background-color: green; }
  body a {
    color: blue; }
'''

B_EXPECTED_CSS = '''\
b i {
  font-size: 20px; }
'''

@suite.test
def compile_filename():
    actual = sass.compile(filename='test/a.sass')
    assert actual == A_EXPECTED_CSS
    with raises(IOError):
        sass.compile(filename='test/not-exist.sass')
    with raises(TypeError):
        sass.compile(filename=1234)
    with raises(TypeError):
        sass.compile(filename=[])


@suite.test
def builder_build_directory():
    temp_path= tempfile.mkdtemp()
    path = os.path.join(temp_path, 'css')
    shutil.copytree('test', path)
    result_files = build_directory(path)
    assert len(result_files) == 2
    assert result_files['a.sass'] == 'a.sass.css'
    with open(os.path.join(path, 'a.sass.css')) as f:
        css = f.read()
    assert css == A_EXPECTED_CSS
    assert result_files['b.sass'] == 'b.sass.css'
    with open(os.path.join(path, 'b.sass.css')) as f:
        css = f.read()
    assert css == B_EXPECTED_CSS
    shutil.rmtree(temp_path)
