from Products.Five.browser import BrowserView
from Products.TinyMCE.browser.interfaces.anchors import IAnchorView
# Not available in xml.etree
from elementtree import HTMLTreeBuilder
from zope.interface import implements


class ATAnchorView(BrowserView):
    implements(IAnchorView)

    def listAnchorNames(self):
        """Return a list of Anchor names"""
        results = []
        tree = HTMLTreeBuilder.TreeBuilder()
        tree.feed('<root>%s</root>' % self.context.getPrimaryField().getAccessor(self.context)())
        rootnode = tree.close()
        for x in rootnode.getiterator():
            if x.tag == "a":
                if "name" in x.keys():
                    results.append(x.attrib['name'])
        return results
