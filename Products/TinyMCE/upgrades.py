from zope.component import getUtility
from Products.TinyMCE.interfaces.utility import ITinyMCE

def upgrade_10_to_11(setuptool):
    """Upgrade TinyMCE from 1.0 to 1.1"""
    
    # http://plone.org/products/tinymce/issues/26
    tinymce = getUtility(ITinyMCE)
    tinymce.styles = tinymce.styles.replace(u'Pull-quote|div|pullquote', u'Pull-quote|blockquote|pullquote')
    
    # Add entity_encoding property
    tinymce.entity_encoding = u"raw"