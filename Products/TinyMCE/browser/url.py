from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from zope.component import getUtility
from Products.Five.browser import BrowserView

from Products.TinyMCE.browser.interfaces.url import ITinyMCEUrl

class TinyMCEUrl(BrowserView):
    """TinyMCE Url"""
    implements(ITinyMCEUrl)

    def getPathByUID(self):
        """Returns the path of an object specified in the request by UID"""

        context = self.context
        request = context.REQUEST

        if not hasattr(request, 'uid'):
            return ""

        uid = request['uid']

        reference_tool = getToolByName(context, 'reference_catalog')
        obj = reference_tool.lookupObject(uid)

        if obj:
            return obj.absolute_url()

        return ""
