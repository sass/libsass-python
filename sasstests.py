# -*- coding: utf-8 -*-
from __future__ import with_statement

import collections
import glob
import json
import os
import os.path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import warnings

from six import PY3, StringIO, b, text_type
from werkzeug.test import Client
from werkzeug.wrappers import Response

import sass
import sassc
from sassutils.builder import Manifest, build_directory
from sassutils.wsgi import SassMiddleware


if os.sep != '/' and os.altsep:
    def normalize_path(path):
        path = os.path.abspath(os.path.normpath(path))
        return path.replace(os.sep, os.altsep)

    def normalize_source_map_path(path):
        """To workaround strange path separators made by libsass ---
        which seems a bug of libsass on win32.

        """
        return path.replace(os.altsep, '//')
else:
    def normalize_path(path):
        return path

    normalize_source_map_path = normalize_path


A_EXPECTED_CSS = '''\
body {
  background-color: green; }
  body a {
    color: blue; }
'''

A_EXPECTED_CSS_WITH_MAP = '''\
/* line 6, SOURCE */
body {
  background-color: green; }
  /* line 8, SOURCE */
  body a {
    color: blue; }

/*# sourceMappingURL=../a.scss.css.map */'''

A_EXPECTED_MAP = {
    'version': 3,
    'file': 'test/a.css',
    'sources': [normalize_source_map_path('test/a.scss')],
    'names': [],
    'mappings': ';AAKA;EAHE,kBAAkB;;EAIpB,KAAK;IAED,OAAO'
}

B_EXPECTED_CSS = '''\
b i {
  font-size: 20px; }
'''

B_EXPECTED_CSS_WITH_MAP = '''\
/* line 2, SOURCE */
b i {
  font-size: 20px; }

/*# sourceMappingURL=../css/b.scss.css.map */'''

C_EXPECTED_CSS = '''\
body {
  background-color: green; }
  body a {
    color: blue; }

h1 a {
  color: green; }
'''

D_EXPECTED_CSS = '''\
body {
  background-color: green; }
  body a {
    font: '나눔고딕', sans-serif; }
'''

D_EXPECTED_CSS_WITH_MAP = '''\
/* line 6, SOURCE */
body {
  background-color: green; }
  /* line 8, SOURCE */
  body a {
    font: '나눔고딕', sans-serif; }

/*# sourceMappingURL=../css/d.scss.css.map */'''

E_EXPECTED_CSS = '''\
a {
  color: red; }
'''

SUBDIR_RECUR_EXPECTED_CSS = '''\
body p {
  color: blue; }
'''

utf8_if_py3 = {'encoding': 'utf-8'} if PY3 else {}


class SassTestCase(unittest.TestCase):

    def test_version(self):
        assert re.match(r'^\d+\.\d+\.\d+$', sass.__version__)

    def test_output_styles(self):
        if hasattr(collections, 'Mapping'):
            assert isinstance(sass.OUTPUT_STYLES, collections.Mapping)
        assert 'nested' in sass.OUTPUT_STYLES

    def test_and_join(self):
        self.assertEqual(
            'Korea, Japan, China, and Taiwan',
            sass.and_join(['Korea', 'Japan', 'China', 'Taiwan'])
        )
        self.assertEqual(
            'Korea, and Japan',
            sass.and_join(['Korea', 'Japan'])
        )
        self.assertEqual('Korea', sass.and_join(['Korea']))
        self.assertEqual('', sass.and_join([]))


class CompileTestCase(unittest.TestCase):

    def test_compile_required_arguments(self):
        self.assertRaises(TypeError, sass.compile)


    def test_compile_takes_only_keywords(self):
        self.assertRaises(TypeError, sass.compile, 'a { color: blue; }')

    def test_compile_exclusive_arguments(self):
        self.assertRaises(TypeError, sass.compile,
                          string='a { color: blue; }', filename='test/a.scss')
        self.assertRaises(TypeError, sass.compile,
                          string='a { color: blue; }', dirname='test/')
        self.assertRaises(TypeError,  sass.compile,
                          filename='test/a.scss', dirname='test/')

    def test_compile_invalid_output_style(self):
        self.assertRaises(TypeError, sass.compile,
                          string='a { color: blue; }',
                          output_style=['compact'])
        self.assertRaises(TypeError,  sass.compile,
                          string='a { color: blue; }', output_style=123j)
        self.assertRaises(ValueError,  sass.compile,
                          string='a { color: blue; }', output_style='invalid')

    def test_compile_invalid_source_comments(self):
        self.assertRaises(TypeError, sass.compile,
                          string='a { color: blue; }',
                          source_comments=['line_numbers'])
        self.assertRaises(TypeError,  sass.compile,
                          string='a { color: blue; }', source_comments=123j)
        self.assertRaises(TypeError,  sass.compile,
                          string='a { color: blue; }',
                          source_comments='invalid')

    def test_compile_invalid_image_path(self):
        self.assertRaises(TypeError, sass.compile,
                          string='a { color: blue; }', image_path=[])
        self.assertRaises(TypeError, sass.compile,
                          string='a { color: blue; }', image_path=123)

    def test_compile_string(self):
        actual = sass.compile(string='a { b { color: blue; } }')
        assert actual == 'a b {\n  color: blue; }\n'
        commented = sass.compile(string='''a {
            b { color: blue; }
            color: red;
        }''', source_comments=True)
        assert commented == '''/* line 1, stdin */
a {
  color: red; }
  /* line 2, stdin */
  a b {
    color: blue; }
'''
        actual = sass.compile(string=u'a { color: blue; } /* 유니코드 */')
        self.assertEqual(
            u'''a {
  color: blue; }

/* 유니코드 */''',
            actual
        )
        self.assertRaises(sass.CompileError, sass.compile,
                          string='a { b { color: blue; }')
        # sass.CompileError should be a subtype of ValueError
        self.assertRaises(ValueError, sass.compile,
                          string='a { b { color: blue; }')
        self.assertRaises(TypeError, sass.compile, string=1234)
        self.assertRaises(TypeError, sass.compile, string=[])

    def test_compile_string_deprecated_source_comments_line_numbers(self):
        source = '''a {
            b { color: blue; }
            color: red;
        }'''
        expected = sass.compile(string=source, source_comments=True)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            actual = sass.compile(string=source,
                                  source_comments='line_numbers')
            self.assertEqual(1, len(w))
            assert issubclass(w[-1].category, DeprecationWarning)
        self.assertEqual(expected, actual)

    def test_compile_filename(self):
        actual = sass.compile(filename='test/a.scss')
        assert actual == A_EXPECTED_CSS
        actual = sass.compile(filename='test/c.scss')
        assert actual == C_EXPECTED_CSS
        actual = sass.compile(filename='test/d.scss')
        if text_type is str:
            self.assertEqual(D_EXPECTED_CSS, actual)
        else:
            self.assertEqual(D_EXPECTED_CSS.decode('utf-8'), actual)
        actual = sass.compile(filename='test/e.scss')
        assert actual == E_EXPECTED_CSS
        self.assertRaises(IOError, sass.compile,
                          filename='test/not-exist.sass')
        self.assertRaises(TypeError, sass.compile, filename=1234)
        self.assertRaises(TypeError, sass.compile, filename=[])

    def test_compile_source_map(self):
        filename = 'test/a.scss'
        actual, source_map = sass.compile(
            filename=filename,
            source_map_filename='a.scss.css.map'
        )
        self.assertEqual(
            A_EXPECTED_CSS_WITH_MAP.replace(
                'SOURCE',
                normalize_path(os.path.abspath(filename))
            ),
            actual
        )
        self.assertEqual(
            A_EXPECTED_MAP,
            json.loads(source_map)
        )

    def test_compile_source_map_deprecated_source_comments_map(self):
        filename = 'test/a.scss'
        expected, expected_map = sass.compile(
            filename=filename,
            source_map_filename='a.scss.css.map'
        )
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            actual, actual_map = sass.compile(
                filename=filename,
                source_comments='map',
                source_map_filename='a.scss.css.map'
            )
            self.assertEqual(1, len(w))
            assert issubclass(w[-1].category, DeprecationWarning)
        self.assertEqual(expected, actual)
        self.assertEqual(expected_map, actual_map)

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

    def setUp(self):
        self.temp_path = tempfile.mkdtemp()
        self.sass_path = os.path.join(self.temp_path, 'sass')
        self.css_path = os.path.join(self.temp_path, 'css')
        shutil.copytree('test', self.sass_path)

    def tearDown(self):
        shutil.rmtree(self.temp_path)

    def test_builder_build_directory(self):
        css_path = self.css_path
        result_files = build_directory(self.sass_path, css_path)
        self.assertEqual(6, len(result_files))
        self.assertEqual('a.scss.css', result_files['a.scss'])
        with open(os.path.join(css_path, 'a.scss.css'), **utf8_if_py3) as f:
            css = f.read()
        self.assertEqual(A_EXPECTED_CSS, css)
        self.assertEqual('b.scss.css', result_files['b.scss'])
        with open(os.path.join(css_path, 'b.scss.css'), **utf8_if_py3) as f:
            css = f.read()
        self.assertEqual(B_EXPECTED_CSS, css)
        self.assertEqual('c.scss.css', result_files['c.scss'])
        with open(os.path.join(css_path, 'c.scss.css'), **utf8_if_py3) as f:
            css = f.read()
        self.assertEqual(C_EXPECTED_CSS, css)
        self.assertEqual('d.scss.css', result_files['d.scss'])
        with open(os.path.join(css_path, 'd.scss.css'), **utf8_if_py3) as f:
            css = f.read()
        self.assertEqual(D_EXPECTED_CSS, css)
        self.assertEqual('e.scss.css', result_files['e.scss'])
        with open(os.path.join(css_path, 'e.scss.css'), **utf8_if_py3) as f:
            css = f.read()
        self.assertEqual(E_EXPECTED_CSS, css)
        self.assertEqual(
            os.path.join('subdir', 'recur.scss.css'),
            result_files[os.path.join('subdir', 'recur.scss')]
        )
        with open(os.path.join(css_path, 'subdir', 'recur.scss.css'),
                  **utf8_if_py3) as f:
            css = f.read()
        self.assertEqual(SUBDIR_RECUR_EXPECTED_CSS, css)

    def test_output_style(self):
        css_path = self.css_path
        result_files = build_directory(self.sass_path, css_path,
                                       output_style='compressed')
        self.assertEqual(6, len(result_files))
        self.assertEqual('a.scss.css', result_files['a.scss'])
        with open(os.path.join(css_path, 'a.scss.css'), **utf8_if_py3) as f:
            css = f.read()
        self.assertEqual('body{background-color:green}body a{color:blue}',
                         css)


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

    def test_build_one(self):
        d = tempfile.mkdtemp()
        src_path = os.path.join(d, 'test')
        test_source_path = lambda *path: normalize_path(
            os.path.join(d, 'test', *path)
        )
        replace_source_path = lambda s, name: s.replace(
            'SOURCE',
            test_source_path(name)
        )
        try:
            shutil.copytree('test', src_path)
            m = Manifest(sass_path='test', css_path='css')
            m.build_one(d, 'a.scss')
            with open(os.path.join(d, 'css', 'a.scss.css')) as f:
                self.assertEqual(A_EXPECTED_CSS, f.read())
            m.build_one(d, 'b.scss', source_map=True)
            with open(os.path.join(d, 'css', 'b.scss.css'),
                      **utf8_if_py3) as f:
                self.assertEqual(
                    replace_source_path(B_EXPECTED_CSS_WITH_MAP, 'b.scss'),
                    f.read()
                )
            self.assert_json_file(
                {
                    'version': 3,
                    'file': '../test/b.css',
                    'sources': [normalize_source_map_path('../test/b.scss')],
                    'names': [],
                    'mappings': ';AAAA,EAAE;EAEE,WAAW'
                },
                os.path.join(d, 'css', 'b.scss.css.map')
            )
            m.build_one(d, 'd.scss', source_map=True)
            with open(os.path.join(d, 'css', 'd.scss.css'),
                      **utf8_if_py3) as f:
                self.assertEqual(
                    replace_source_path(D_EXPECTED_CSS_WITH_MAP, 'd.scss'),
                    f.read()
                )
            self.assert_json_file(
                {
                    'version': 3,
                    'file': '../test/d.css',
                    'sources': [normalize_source_map_path('../test/d.scss')],
                    'names': [],
                    'mappings': ';AAKA;EAHE,kBAAkB;;EAIpB,KAAK;IAED,MAAM'
                },
                os.path.join(d, 'css', 'd.scss.css.map')
            )
        finally:
            shutil.rmtree(d)

    def assert_json_file(self, expected, filename):
        with open(filename) as f:
            try:
                tree = json.load(f)
            except ValueError as e:
                f.seek(0)
                msg = '{0!s}\n\n{1}:\n\n{2}'.format(e, filename, f.read())
                raise ValueError(msg)
        self.assertEqual(expected, tree)


class WsgiTestCase(unittest.TestCase):

    @staticmethod
    def sample_wsgi_app(environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return environ['PATH_INFO'],

    def test_wsgi_sass_middleware(self):
        css_dir = tempfile.mkdtemp()
        src_dir = os.path.join(css_dir, 'src')
        shutil.copytree('test', src_dir)
        try:
            app = SassMiddleware(self.sample_wsgi_app, {
                __name__: (src_dir, css_dir, '/static')
            })
            client = Client(app, Response)
            r = client.get('/asdf')
            self.assertEqual(200, r.status_code)
            self.assert_bytes_equal(b'/asdf', r.data)
            self.assertEqual('text/plain', r.mimetype)
            r = client.get('/static/a.scss.css')
            self.assertEqual(200, r.status_code)
            src_path = normalize_path(os.path.join(src_dir, 'a.scss'))
            self.assert_bytes_equal(
                b(A_EXPECTED_CSS_WITH_MAP.replace('SOURCE', src_path)),
                r.data
            )
            self.assertEqual('text/css', r.mimetype)
            r = client.get('/static/not-exists.sass.css')
            self.assertEqual(200, r.status_code)
            self.assert_bytes_equal(b'/static/not-exists.sass.css', r.data)
            self.assertEqual('text/plain', r.mimetype)
        finally:
            shutil.rmtree(css_dir)

    def assert_bytes_equal(self, expected, actual, *args):
        self.assertEqual(expected.replace(b'\r\n', b'\n'),
                         actual.replace(b'\r\n', b'\n'),
                         *args)


class DistutilsTestCase(unittest.TestCase):

    def tearDown(self):
        for filename in self.list_built_css():
            os.remove(filename)

    def css_path(self, *args):
        return os.path.join(
            os.path.dirname(__file__),
            'testpkg', 'testpkg', 'static', 'css',
            *args
        )

    def list_built_css(self):
        return glob.glob(self.css_path('*.scss.css'))

    def build_sass(self, *args):
        testpkg_path = os.path.join(os.path.dirname(__file__), 'testpkg')
        return subprocess.call(
            [sys.executable, 'setup.py', 'build_sass'] + list(args),
            cwd=os.path.abspath(testpkg_path)
        )

    def test_build_sass(self):
        rv = self.build_sass()
        self.assertEqual(0, rv)
        self.assertEqual(
            ['a.scss.css'],
            list(map(os.path.basename, self.list_built_css()))
        )
        with open(self.css_path('a.scss.css')) as f:
            self.assertEqual(
                'p a {\n  color: red; }\np b {\n  color: blue; }\n',
                f.read()
            )

    def test_output_style(self):
        rv = self.build_sass('--output-style', 'compressed')
        self.assertEqual(0, rv)
        with open(self.css_path('a.scss.css')) as f:
            self.assertEqual(
                'p a{color:red}p b{color:blue}',
                f.read()
            )


class SasscTestCase(unittest.TestCase):

    def setUp(self):
        self.out = StringIO()
        self.err = StringIO()

    def test_no_args(self):
        exit_code = sassc.main(['sassc', ], self.out, self.err)
        self.assertEqual(2, exit_code)
        err = self.err.getvalue()
        assert err.strip().endswith('error: too few arguments'), \
               'actual error message is: ' + repr(err)
        self.assertEqual('', self.out.getvalue())

    def test_three_args(self):
        exit_code = sassc.main(
            ['sassc', 'a.scss', 'b.scss', 'c.scss'],
            self.out, self.err
        )
        self.assertEqual(2, exit_code)
        err = self.err.getvalue()
        assert err.strip().endswith('error: too many arguments'), \
               'actual error message is: ' + repr(err)
        self.assertEqual('', self.out.getvalue())

    def test_sassc_stdout(self):
        exit_code = sassc.main(['sassc', 'test/a.scss'], self.out, self.err)
        self.assertEqual(0, exit_code)
        self.assertEqual('', self.err.getvalue())
        self.assertEqual(A_EXPECTED_CSS.strip(), self.out.getvalue().strip())

    def test_sassc_output(self):
        fd, tmp = tempfile.mkstemp('.css')
        try:
            os.close(fd)
            exit_code = sassc.main(['sassc', 'test/a.scss', tmp],
                                   self.out, self.err)
            self.assertEqual(0, exit_code)
            self.assertEqual('', self.err.getvalue())
            self.assertEqual('', self.out.getvalue())
            with open(tmp) as f:
                self.assertEqual(A_EXPECTED_CSS.strip(), f.read().strip())
        finally:
            os.remove(tmp)

    def test_sassc_output_unicode(self):
        fd, tmp = tempfile.mkstemp('.css')
        try:
            os.close(fd)
            exit_code = sassc.main(['sassc', 'test/d.scss', tmp],
                                   self.out, self.err)
            self.assertEqual(0, exit_code)
            self.assertEqual('', self.err.getvalue())
            self.assertEqual('', self.out.getvalue())
            with open(tmp, **utf8_if_py3) as f:
                self.assertEqual(
                    D_EXPECTED_CSS.strip(),
                    f.read().strip()
                )
        finally:
            os.remove(tmp)

    def test_sassc_source_map_without_css_filename(self):
        exit_code = sassc.main(['sassc', '-m', 'a.scss'], self.out, self.err)
        self.assertEqual(2, exit_code)
        err = self.err.getvalue()
        assert err.strip().endswith('error: -m/-g/--sourcemap requires '
                                    'the second argument, the output css '
                                    'filename.'), \
               'actual error message is: ' + repr(err)
        self.assertEqual('', self.out.getvalue())

    def test_sassc_sourcemap(self):
        tmp_dir = tempfile.mkdtemp()
        src_dir = os.path.join(tmp_dir, 'test')
        shutil.copytree('test', src_dir)
        src_filename = os.path.join(src_dir, 'a.scss')
        out_filename = os.path.join(tmp_dir, 'a.scss.css')
        try:
            exit_code = sassc.main(
                ['sassc', '-m', src_filename, out_filename],
                self.out, self.err
            )
            self.assertEqual(0, exit_code)
            self.assertEqual('', self.err.getvalue())
            self.assertEqual('', self.out.getvalue())
            with open(out_filename) as f:
                self.assertEqual(
                    A_EXPECTED_CSS_WITH_MAP.replace(
                        'SOURCE', normalize_path(src_filename)
                    ),
                    f.read().strip()
                )
            with open(out_filename + '.map') as f:
                self.assertEqual(
                    dict(A_EXPECTED_MAP, sources=None),
                    dict(json.load(f), sources=None)
                )
        finally:
            shutil.rmtree(tmp_dir)


test_cases = [
    SassTestCase,
    CompileTestCase,
    BuilderTestCase,
    ManifestTestCase,
    WsgiTestCase,
    DistutilsTestCase,
    SasscTestCase
]
loader = unittest.defaultTestLoader
suite = unittest.TestSuite()
for test_case in test_cases:
    suite.addTests(loader.loadTestsFromTestCase(test_case))
