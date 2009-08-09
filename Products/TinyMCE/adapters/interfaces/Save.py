from zope.interface import Interface

class ISave(Interface):
    """Saves the richedit field"""

    def __init__(self, context):
        """Constructor"""

    def save(self, text, fieldname):
        """Saves the specified richedit field"""
