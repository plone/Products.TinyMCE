#Fix according to http://code.google.com/p/dexterity/issues/detail?id=274

from Products.Five.browser import BrowserView
from Products.TinyMCE.browser.interfaces.anchors import IAnchorView
from elementtree import HTMLTreeBuilder
from plone.dexterity.utils import iterSchemata
from plone.rfc822.interfaces import IPrimaryField
from zope.interface import implements
from zope.schema import getFieldsInOrder


class DexterityAnchorView(BrowserView):
    """View to list anchors.

    Taken over from Products/TinyMCE/browser/atanchors.py.
    Changed to work for dexterity items.
    """
    implements(IAnchorView)

    def listAnchorNames(self, fieldname=None):
        """Return a list of Anchor names"""
        results = []
        tree = HTMLTreeBuilder.TreeBuilder()
        content_field = None
        for schema in iterSchemata(self.context):
            if content_field is not None:
                break
            for name, field in getFieldsInOrder(schema):
                if (not fieldname and IPrimaryField.providedBy(field)) or name == fieldname:
                    content_field = field
                    break
        if content_field is None:
            return []
        try:
            content = content_field.get(self.context).output
        except AttributeError:
            # Not a text field.
            return []
        tree.feed('<root>%s</root>' % content)
        rootnode = tree.close()
        for x in rootnode.getiterator():
            if x.tag == "a":
                if "name" in x.keys():
                    results.append(x.attrib['name'])
        return results
