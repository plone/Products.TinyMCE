from Products.Five.browser import BrowserView
from Products.TinyMCE.browser.interfaces.anchors import IAnchorView
from zope.interface import implements

try:
    from lxml.html import parse
except ImportError:
    from elementtree.HTMLTreeBuilder import parse


class ATAnchorView(BrowserView):
    implements(IAnchorView)

    def listAnchorNames(self, fieldname=None):
        """Return a list of Anchor names"""
        results = []
        if not fieldname:
            field = self.context.getPrimaryField()
        else:
            field = self.context.getField(fieldname)

        htmlsnippet = field.getAccessor(self.context)()
        try:
            tree = parse('<root>%s</root>' % htmlsnippet)
        except:
            return results
        for x in tree.getroot().getiterator():
            if x.tag == "a":
                if "name" in x.keys():
                    results.append(x.attrib['name'])
        return results
