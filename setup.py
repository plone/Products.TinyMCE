from setuptools import setup, find_packages

setup(name='Products.TinyMCE',
    version='1.4.4.dev0',
    description=("Adds support for TinyMCE, a platform independent web based "
                 "Javascript HTML WYSIWYG editor, to Plone."),
    long_description=(open("README.rst").read() + '\n\n' +
                      open("HISTORY.rst").read()),
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
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
        'plone.fieldsets',
        'Products.ResourceRegistries',
        'zope.app.content',
        'zope.schema>=3.5.4',
        # depends on *either* elementtree or lxml...
        # we can expect one of those in all versions of Plone
    ],
    extras_require={
        'test': ['plone.app.testing',
                 'zope.testing',
                 'unittest2',
                 'Pillow',
                 'plone.app.contenttypes'],
        'docs': ['sphinx'],
    },
)
