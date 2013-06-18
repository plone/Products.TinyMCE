from Products.CMFCore.utils import getToolByName
from Products.TinyMCE.setuphandlers import uninstall_mimetype_and_transforms
from plone.outputfilters.setuphandlers import install_mimetype_and_transforms
try:
    from zope.component.hooks import getSite
    getSite   # pyflakes
except ImportError:
    from zope.app.component.hooks import getSite


def meta_types_to_portal_types(meta_types):
    """Convert meta types to portal types"""
    meta_types = meta_types.replace(u'ATTopic', u'Topic')
    meta_types = meta_types.replace(u'ATEvent', u'Event')
    meta_types = meta_types.replace(u'ATFile', u'File')
    meta_types = meta_types.replace(u'ATFolder', u'Folder')
    meta_types = meta_types.replace(u'ATImage', u'Image')
    meta_types = meta_types.replace(u'ATBTreeFolder', u'Large Plone Folder')
    meta_types = meta_types.replace(u'ATNewsItem', u'News Item')
    meta_types = meta_types.replace(u'ATDocument', u'Document')
    return meta_types


def upgrade_10_to_11(setuptool):
    """Upgrade TinyMCE from 1.0 to 1.1"""

    # http://plone.org/products/tinymce/issues/26
    tinymce = getToolByName(setuptool, 'portal_tinymce')
    tinymce.styles = tinymce.styles.replace(u'Pull-quote|div|pullquote', u'Pull-quote|blockquote|pullquote')
    tinymce.styles = tinymce.styles.replace(u'Discreet|p|discreet', u'Discreet|span|discreet')

    # Add entity_encoding property
    tinymce.entity_encoding = u"raw"

    # Add custom toolbar buttons property
    tinymce.customtoolbarbuttons = u""

    # Add rooted property
    tinymce.rooted = False

    # Convert meta_types to portal_types
    tinymce.containsobjects = meta_types_to_portal_types(tinymce.containsobjects)
    tinymce.containsanchors = meta_types_to_portal_types(tinymce.containsanchors)
    tinymce.linkable = meta_types_to_portal_types(tinymce.linkable)
    tinymce.imageobjects = meta_types_to_portal_types(tinymce.imageobjects)

    # Unregister old js and register new js
    setuptool.runAllImportStepsFromProfile('profile-Products.TinyMCE:upgrade_10_to_11')

    # Add definitionlist property
    tinymce.toolbar_definitionlist = True

    # Remove autoresize bottom margin
    try:
        del tinymce.autoresize_bottom_margin
    except AttributeError:
        pass


def upgrade_11_to_2(setuptool):
    site = getSite()
    uninstall_mimetype_and_transforms(site)
    install_mimetype_and_transforms(site)


def upgrade_12_to_13(setuptool):
    # plonebrowser replaces ploneimage & plonelink
    tinymce = getToolByName(setuptool, 'portal_tinymce')
    plugins = tinymce.customplugins.split()
    if u'plonebrowser' not in plugins:
        plugins.append(u'plonebrowser')
    plugins = filter(lambda x: x != u'plonelink' and x != u'ploneimage', plugins)
    tinymce.customplugins = '\n'.join(plugins)

    # Unregister old js and kss and register new js
    setuptool.runAllImportStepsFromProfile('profile-Products.TinyMCE:upgrade_12_to_13')


def upgrade_to_profile_5(setuptool):
    setuptool.runAllImportStepsFromProfile('profile-Products.TinyMCE:upgrade_to_profile_5')


def upgrade_to_profile_6(setuptool):
    setuptool.runAllImportStepsFromProfile('profile-Products.TinyMCE:upgrade_to_profile_6')


def upgrade_to_profile_7(setuptool):
    # https://dev.plone.org/ticket/13458
    tinymce = getToolByName(setuptool, 'portal_tinymce')
    tinymce.styles = tinymce.styles.replace(u'Heading|h2| ', u'Heading|h2|')
    tinymce.styles = tinymce.styles.replace(u'Subheading|h3| ', u'Subheading|h3|')
    tinymce.styles = tinymce.styles.replace(u'Literal|pre| ', u'Literal|pre|')
    tinymce.styles = tinymce.styles.replace(u'Definition term|dt| ', u'Definition term|dt|')
    tinymce.styles = tinymce.styles.replace(u'Definition description|dd| ', u'Definition description|dd|')
    tinymce.styles = tinymce.styles.replace(u'Heading cell|th| ', u'Heading cell|th|')
