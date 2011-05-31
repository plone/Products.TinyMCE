from zope.interface import Interface


class IJSONDetails(Interface):
    """Return details of the current object in JSON"""

    def __init__(self, context):
        """Constructor"""

    def getDetails(self):
        """Returns the actual details"""
