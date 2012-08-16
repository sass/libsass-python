from __future__ import with_statement
from attest import assert_hook

from attest import Tests, raises

from sass import BaseContext, Options


suite = Tests()


@suite.test
def options_output_style():
    for style in 'nested', 'expanded', 'compact', 'compressed':
        o = Options(output_style=style, include_paths='a:b', image_path='')
        assert o.output_style == style
    with raises(TypeError):
        Options(output_style=None, include_paths='a:b', image_path='')
    with raises(TypeError):
        Options(output_style=123, include_paths='a:b', image_path='')
    with raises(TypeError):
        Options(output_style=['abc'], include_paths='a:b', image_path='')
    with raises(ValueError):
        Options(output_style='abc', include_paths='a:b', image_path='')


@suite.test
def options_include_paths():
    o = Options('nested', include_paths='ab/cd:de/fg', image_path='')
    assert o.include_paths == ['ab/cd', 'de/fg']
    o = Options('nested', include_paths=['li/st', 'te/st'], image_path='')
    assert o.include_paths == ['li/st', 'te/st']
    o = Options('nested', include_paths=('tup/le', 'te/st'), image_path='')
    assert o.include_paths == ['tup/le', 'te/st']
    with raises(TypeError):
        Options('nested', include_paths=None, image_path='a/b')
    with raises(TypeError):
        Options('nested', include_paths=123, image_path='a/b')


@suite.test
def options_image_path():
    o = Options('nested', include_paths='a:b', image_path='image/path')
    assert o.image_path == 'image/path'
    with raises(TypeError):
        Options('nested', include_paths='a:b', image_path=None)
    with raises(TypeError):
        Options('nested', include_paths='a:b', image_path=123)
    with raises(TypeError):
        Options('nested', include_paths='a:b', image_path=['a/b', 'c/d'])


@suite.test
def base_context_init():
    with raises(TypeError):
        BaseContext()
    assert hasattr(BaseContext, 'options')
    assert callable(BaseContext.compile)
