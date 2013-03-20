#Fix according to http://code.google.com/p/dexterity/issues/detail?id=274

from Products.Five.browser import BrowserView
from Products.TinyMCE.browser.interfaces.anchors import IAnchorView
from plone.dexterity.utils import iterSchemata
from plone.rfc822.interfaces import IPrimaryField
from zope.interface import implements
from zope.schema import getFieldsInOrder

try:
    from lxml.html import fromstring
    fromstring     # pyflakes
    SEARCHPATTERN = "a"
except ImportError:
    from elementtree import HTMLTreeBuilder

    def fromstring(text):
        parser = HTMLTreeBuilder.TreeBuilder()
        text = '<root>%s</root>' % text
        parser.feed(text)
        return parser.close()

    SEARCHPATTERN = "*/a"


class DexterityAnchorView(BrowserView):
    """View to list anchors.

    Taken over from Products/TinyMCE/browser/atanchors.py.
    Changed to work for dexterity items.
    """
    implements(IAnchorView)

    def listAnchorNames(self, fieldname=None):
        """Return a list of Anchor names"""
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
        try:
            tree = fromstring(content)
        except ConflictError:
            raise
        except Exception:
            return []
        return [anchor.get('name') for anchor in tree.findall(SEARCHPATTERN)
                if "name" in anchor.keys()]
