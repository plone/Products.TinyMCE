from zope.interface import Interface


class IAnchorView(Interface):
    """Information about the anchors in the content of a page.
    @@content_anchors
    """

    def listAnchorNames(self):
        """Return a list of Anchor names"""
