from zope.interface import implements
from zope.component import adapts
from Products.CMFCore.utils import getToolByName

from Products.TinyMCE.adapters.interfaces.Save import ISave
from Products.CMFPlone import utils
from Acquisition import aq_inner

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
