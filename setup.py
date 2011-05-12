from setuptools import setup, find_packages
import os
import sys

version = '1.2.6'

if sys.version_info[0] == 2 and sys.version_info[1] < 6:
    requires = ['simplejson']
else:
    requires = []

setup(name='Products.TinyMCE',
      version=version,
      description="Adds support for TinyMCE, a platform independent web based Javascript HTML WYSIWYG editor, to Plone.",
      long_description=open("README.txt").read() + "\n\n" +
                       open(os.path.join("docs", "INSTALL.txt")).read() + "\n\n" +
                       open("CHANGES.txt").read() + "\n\n" +
                       open(os.path.join("docs", "CONTRIBUTORS.txt")).read(),
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
      ] + requires,
      extras_require = {
            'test':  ['Products.PloneTestCase'],
            },
      )
