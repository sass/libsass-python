from setuptools import setup


setup(
    name='testpkg',
    packages=['testpkg'],
    sass_manifests={
        'testpkg': ('static/scss', 'static/css')
    },
    setup_requires=['libsass']
)
