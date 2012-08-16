from __future__ import with_statement
from attest import assert_hook

from attest import Tests, raises

from sass import Options


suite = Tests()


@suite.test
def options_include_paths():
    o = Options(include_paths='ab/cd:de/fg', image_path='')
    assert o.include_paths == ['ab/cd', 'de/fg']
    o = Options(include_paths=['li/st', 'te/st'], image_path='')
    assert o.include_paths == ['li/st', 'te/st']
    o = Options(include_paths=('tup/le', 'te/st'), image_path='')
    assert o.include_paths == ['tup/le', 'te/st']
    with raises(TypeError):
        Options(include_paths=None, image_path='a/b')
    with raises(TypeError):
        Options(include_paths=123, image_path='a/b')


@suite.test
def options_image_path():
    o = Options(include_paths='a:b', image_path='image/path')
    assert o.image_path == 'image/path'
    with raises(TypeError):
        Options(include_paths='a:b', image_path=None)
    with raises(TypeError):
        Options(include_paths='a:b', image_path=123)
    with raises(TypeError):
        Options(include_paths='a:b', image_path=['a/b', 'c/d'])
