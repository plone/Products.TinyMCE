from ZODB.POSException import ConflictError
from Products.Five.browser import BrowserView
from Products.TinyMCE.browser.interfaces.anchors import IAnchorView
from zope.interface import implements

try:
    from lxml.html import fromstring
    fromstring     # pyflakes
    SEARCHPATTERN = ".//a"
except ImportError:
    from elementtree import HTMLTreeBuilder

    def fromstring(text):
        parser = HTMLTreeBuilder.TreeBuilder()
        text = '<root>%s</root>' % text
        parser.feed(text)
        return parser.close()

    SEARCHPATTERN = "*/a"


class ATAnchorView(BrowserView):
    implements(IAnchorView)

    def listAnchorNames(self, fieldname=None):
        """Return a list of Anchor names"""
        if not fieldname:
            field = self.context.getPrimaryField()
        else:
            field = self.context.getField(fieldname)

        if field is None:
            return []

        htmlsnippet = field.getAccessor(self.context)()
        try:
            tree = fromstring(htmlsnippet)
        except ConflictError:
            raise
        except Exception:
            return []

        anchors = []
        for anchor in tree.findall(SEARCHPATTERN):
            if "name" in anchor.keys():
                anchors.append(anchor.get('name'))
            if "id" in anchor.keys():
                anchors.append(anchor.get('id'))
        return anchors
