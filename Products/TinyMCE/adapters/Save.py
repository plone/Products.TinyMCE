from zope.interface import implements
from Products.TinyMCE.adapters.interfaces.Save import ISave


class Save(object):
    """Saves the richedit field"""

    implements(ISave)

    def __init__(self, context):
        """Constructor"""

        self.context = context

    def save(self, text, fieldname):
        """Saves the specified richedit field"""

        self.context.getField(fieldname).set(self.context, text, mimetype='text/html')

        return "saved"
