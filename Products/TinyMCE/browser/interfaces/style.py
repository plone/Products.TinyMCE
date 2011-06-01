from zope.interface import Interface


class ITinyMCEStyle(Interface):
    """TinyMCE Style"""

    def getStyle(self):
        """Returns a stylesheet with all content styles"""
