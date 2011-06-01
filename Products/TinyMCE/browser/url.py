from zope.interface import implements
from Products.Five.browser import BrowserView
from plone.outputfilters.browser.resolveuid import uuidToObject

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
        obj = uuidToObject(uid)

        if obj:
            return obj.absolute_url()

        return ""
