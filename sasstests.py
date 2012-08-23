from __future__ import with_statement
from attest import assert_hook

import os.path
import re
import shutil
import tempfile

from attest import Tests, raises
from werkzeug.test import Client
from werkzeug.wrappers import Response

import sass
from sassutils.builder import Manifest, build_directory
from sassutils.wsgi import SassMiddleware


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

C_EXPECTED_CSS = '''\
body {
  background-color: green; }
  body a {
    color: blue; }

h1 a {
  color: green; }
'''

@suite.test
def compile_filename():
    actual = sass.compile(filename='test/a.sass')
    assert actual == A_EXPECTED_CSS
    actual = sass.compile(filename='test/c.sass')
    assert actual == C_EXPECTED_CSS
    with raises(IOError):
        sass.compile(filename='test/not-exist.sass')
    with raises(TypeError):
        sass.compile(filename=1234)
    with raises(TypeError):
        sass.compile(filename=[])


@suite.test
def builder_build_directory():
    temp_path= tempfile.mkdtemp()
    sass_path = os.path.join(temp_path, 'sass')
    css_path = os.path.join(temp_path, 'css')
    shutil.copytree('test', sass_path)
    result_files = build_directory(sass_path, css_path)
    assert len(result_files) == 3
    assert result_files['a.sass'] == 'a.sass.css'
    with open(os.path.join(css_path, 'a.sass.css')) as f:
        css = f.read()
    assert css == A_EXPECTED_CSS
    assert result_files['b.sass'] == 'b.sass.css'
    with open(os.path.join(css_path, 'b.sass.css')) as f:
        css = f.read()
    assert css == B_EXPECTED_CSS
    assert result_files['c.sass'] == 'c.sass.css'
    with open(os.path.join(css_path, 'c.sass.css')) as f:
        css = f.read()
    assert css == C_EXPECTED_CSS
    shutil.rmtree(temp_path)


@suite.test
def normalize_manifests():
    manifests = Manifest.normalize_manifests({
        'package': 'sass/path',
        'package.name': ('sass/path', 'css/path'),
        'package.name2': Manifest('sass/path', 'css/path')
    })
    assert len(manifests) == 3
    assert isinstance(manifests['package'], Manifest)
    assert manifests['package'].sass_path == 'sass/path'
    assert manifests['package'].css_path == 'sass/path'
    assert isinstance(manifests['package.name'], Manifest)
    assert manifests['package.name'].sass_path == 'sass/path'
    assert manifests['package.name'].css_path == 'css/path'
    assert isinstance(manifests['package.name2'], Manifest)
    assert manifests['package.name2'].sass_path == 'sass/path'
    assert manifests['package.name2'].css_path == 'css/path'


def sample_wsgi_app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return environ['PATH_INFO'],


@suite.test
def wsgi_sass_middleware():
    css_dir = tempfile.mkdtemp()
    app = SassMiddleware(sample_wsgi_app, {
        __name__: ('test', css_dir, '/static')
    })
    client = Client(app, Response)
    r = client.get('/asdf')
    assert r.status_code == 200
    assert r.data == '/asdf'
    assert r.mimetype == 'text/plain'
    r = client.get('/static/a.sass.css')
    assert r.status_code == 200
    assert r.data == A_EXPECTED_CSS
    assert r.mimetype == 'text/css'
    r = client.get('/static/not-exists.sass.css')
    assert r.status_code == 200
    assert r.data == '/static/not-exists.sass.css'
    assert r.mimetype == 'text/plain'
    shutil.rmtree(css_dir)
