from __future__ import with_statement

import collections
import os.path
import re
import shutil
import tempfile
import unittest

from six import b
from werkzeug.test import Client
from werkzeug.wrappers import Response

import sass
from sassutils.builder import Manifest, build_directory
from sassutils.wsgi import SassMiddleware


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


class SassTestCase(unittest.TestCase):

    def test_version(self):
        assert re.match(r'^\d+\.\d+\.\d+$', sass.__version__)

    def test_output_styles(self):
        if hasattr(collections, 'Mapping'):
            assert isinstance(sass.OUTPUT_STYLES, collections.Mapping)
        assert 'nested' in sass.OUTPUT_STYLES

    def test_and_join(self):
        self.assertEquals(
            'Korea, Japan, China, and Taiwan',
            sass.and_join(['Korea', 'Japan', 'China', 'Taiwan'])
        )
        self.assertEquals(
            'Korea, and Japan',
            sass.and_join(['Korea', 'Japan'])
        )
        self.assertEquals('Korea', sass.and_join(['Korea']))
        self.assertEquals('', sass.and_join([]))


class CompileTestCase(unittest.TestCase):

    def test_compile_required_arguments(self):
        self.assertRaises(TypeError, sass.compile)


    def test_compile_takes_only_keywords(self):
        self.assertRaises(TypeError, sass.compile, 'a { color: blue; }')

    def test_compile_exclusive_arguments(self):
        self.assertRaises(TypeError, sass.compile,
                          string='a { color: blue; }', filename='test/a.sass')
        self.assertRaises(TypeError, sass.compile,
                          string='a { color: blue; }', dirname='test/')
        self.assertRaises(TypeError,  sass.compile,
                          filename='test/a.sass', dirname='test/')

    def test_compile_invalid_output_style(self):
        self.assertRaises(TypeError, sass.compile,
                          string='a { color: blue; }',
                          output_style=['compact'])
        self.assertRaises(TypeError,  sass.compile,
                          string='a { color: blue; }', output_style=123j)
        self.assertRaises(ValueError,  sass.compile,
                          string='a { color: blue; }', output_style='invalid')

    def test_compile_invalid_image_path(self):
        self.assertRaises(TypeError, sass.compile,
                          string='a { color: blue; }', image_path=[])
        self.assertRaises(TypeError, sass.compile,
                          string='a { color: blue; }', image_path=123)

    def test_compile_string(self):
        actual = sass.compile(string='a { b { color: blue; } }')
        assert actual == 'a b {\n  color: blue; }\n'
        self.assertRaises(sass.CompileError, sass.compile,
                          string='a { b { color: blue; }')
        # sass.CompileError should be a subtype of ValueError
        self.assertRaises(ValueError, sass.compile,
                          string='a { b { color: blue; }')
        self.assertRaises(TypeError, sass.compile, string=1234)
        self.assertRaises(TypeError, sass.compile, string=[])

    def test_compile_filename(self):
        actual = sass.compile(filename='test/a.sass')
        assert actual == A_EXPECTED_CSS
        actual = sass.compile(filename='test/c.sass')
        assert actual == C_EXPECTED_CSS
        self.assertRaises(IOError, sass.compile,
                          filename='test/not-exist.sass')
        self.assertRaises(TypeError, sass.compile, filename=1234)
        self.assertRaises(TypeError, sass.compile, filename=[])

    def test_regression_issue_2(self):
        actual = sass.compile(string='''
            @media (min-width: 980px) {
                a {
                    color: red;
                }
            }
        ''')
        normalized = re.sub(r'\s+', '', actual)
        assert normalized == '@media(min-width:980px){a{color:red;}}'

    def test_regression_issue_11(self):
        actual = sass.compile(string='''
            $foo: 3;
            @media (max-width: $foo) {
                body { color: black; }
            }
        ''')
        normalized = re.sub(r'\s+', '', actual)
        assert normalized == '@media(max-width:3){body{color:black;}}'


class BuilderTestCase(unittest.TestCase):

    def test_builder_build_directory(self):
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


class ManifestTestCase(unittest.TestCase):

    def test_normalize_manifests(self):
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


class WsgiTestCase(unittest.TestCase):

    @staticmethod
    def sample_wsgi_app(environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return environ['PATH_INFO'],

    def test_wsgi_sass_middleware(self):
        css_dir = tempfile.mkdtemp()
        app = SassMiddleware(self.sample_wsgi_app, {
            __name__: ('test', css_dir, '/static')
        })
        client = Client(app, Response)
        r = client.get('/asdf')
        self.assertEquals(200, r.status_code)
        self.assertEquals(b'/asdf', r.data)
        self.assertEquals('text/plain', r.mimetype)
        r = client.get('/static/a.sass.css')
        self.assertEquals(200, r.status_code)
        self.assertEquals(b(A_EXPECTED_CSS), r.data)
        self.assertEquals('text/css', r.mimetype)
        r = client.get('/static/not-exists.sass.css')
        self.assertEquals(200, r.status_code)
        self.assertEquals(b'/static/not-exists.sass.css', r.data)
        self.assertEquals('text/plain', r.mimetype)
        shutil.rmtree(css_dir)


test_cases = [
    SassTestCase,
    CompileTestCase,
    BuilderTestCase,
    ManifestTestCase,
    WsgiTestCase
]
loader = unittest.defaultTestLoader
suite = unittest.TestSuite()
for test_case in test_cases:
    suite.addTests(loader.loadTestsFromTestCase(test_case))
