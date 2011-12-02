from setuptools import setup, find_packages
import os
import sys


version = '1.3dev'
open_relative = lambda *x: open(os.path.join(os.path.dirname(__file__), *x)).read()

if sys.version_info[0] == 2 and sys.version_info[1] < 6:
    requires = ['simplejson']
else:
    requires = []

long_description = """
%s

%s

%s

%s
""" % (open_relative("README.txt"),
       open_relative("docs", "INSTALL.txt"),
       open_relative("CHANGES.txt"),
       open_relative("docs", "CONTRIBUTORS.txt"))

setup(name='Products.TinyMCE',
    version=version,
    description="Adds support for TinyMCE, a platform independent web based Javascript HTML WYSIWYG editor, to Plone.",
    long_description=long_description,
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
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
        'elementtree',
        'plone.app.imaging>=1.0.2',
        'plone.outputfilters',
        'Products.ResourceRegistries',
        'Products.Archetypes',
        'zope.schema>=3.5.4'
    ] + requires,
    extras_require={
        'test': ['plone.app.testing', 'unittest2', 'plone.app.dexterity'],
    },
)
