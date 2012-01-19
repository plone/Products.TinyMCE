from zope.interface import implements
from Products.Five.browser import BrowserView
from plone.outputfilters.browser.resolveuid import uuidToObject

from Products.TinyMCE.browser.interfaces.url import ITinyMCEUrl


class TinyMCEUrl(BrowserView):
    """TinyMCE Url"""
    implements(ITinyMCEUrl)

    def getPathByUID(self):
        """Returns the absolute url of an object specified in the request by UID"""

        obj = uuidToObject(self.request.get('uid', ""))
        if obj is not None:
            return obj.absolute_url()
        else:
            self.request.response.setStatus(410)
            return ''
