from Products.PythonScripts.standard import url_quote
from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from zope.component import getUtility
from Products.Five.browser import BrowserView
from Acquisition import aq_inner

from Products.TinyMCE.browser.interfaces.style import ITinyMCEStyle
from Products.TinyMCE.interfaces.utility import ITinyMCE

class TinyMCEStyle(BrowserView):
    """TinyMCE Style"""
    implements(ITinyMCEStyle)

    def getStyle(self):
        """Returns a stylesheet with all content styles"""
        
        registry = getToolByName(aq_inner(self.context), 'portal_css')
        registry_url = registry.absolute_url()
        context = aq_inner(self.context)

        styles = registry.getEvaluatedResources(context)
        skinname = url_quote(aq_inner(self.context).getCurrentSkinName())
        result = []

        for style in styles:
            if style.getMedia() not in ('print', 'projection') and style.getRel()=='stylesheet' :
                src = "<!-- @import url(%s/%s/%s); -->" % (registry_url, skinname, style.getId())
                result.append(src)
        return "\n".join(result)

