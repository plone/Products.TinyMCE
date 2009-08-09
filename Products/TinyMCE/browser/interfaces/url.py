from zope.interface import Interface

class ITinyMCEUrl(Interface):
    """TinyMCE Url"""

    def getPathByUID(self):
        """Returns the path of an object specified in the request by UID"""
