import sys

from setuptools import setup, find_packages

long_description = open("README.rst").read()
long_description += '\n\n'
long_description += open("HISTORY.rst").read()

if sys.version_info[0] == 2 and sys.version_info[1] < 6:
    requires = ['simplejson']
else:
    requires = []

setup(name='Products.TinyMCE',
    version='1.3.11',
    description="Adds support for TinyMCE, a platform independent web based Javascript HTML WYSIWYG editor, to Plone.",
    long_description=long_description,
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='editor editors tinymce wysiwyg',
    author='Four Digits',
    author_email='rob@fourdigits.nl',
    url='http://plone.org/products/tinymce',
    license='LGPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'plone.app.imaging>=1.0.2',
        'plone.outputfilters',
        'plone.namedfile',
        'plone.app.layout>=2.3.7',
        'plone.caching',
        'Products.ResourceRegistries',
        'zope.app.content',
        'zope.schema>=3.5.4',
        # depends on *either* elementtree or lxml...
        # we can expect one of those in all versions of Plone
    ] + requires,
    extras_require={
        'test': ['plone.app.testing',
                 'zope.testing',
                 'unittest2',
                 'Pillow',
                 'plone.app.dexterity'],
        'docs': ['sphinx'],
    },
)
