"""Shortcuts implementation for Plone"""

from Acquisition import aq_parent, aq_inner
from Products.TinyMCE.interfaces.utility import _
from Products.CMFCore.utils import getToolByName
from zope.i18n import translate


class CurrentFolderShortcut(object):
    """Provides shortcut to current folder"""
    title = _(u'Current Folder')

    def render(self, context):
        portal_factory = getToolByName(context, 'portal_factory')
        if portal_factory.isTemporary(context):
            # Fix current folder URL on creation
            url = aq_parent(aq_parent(aq_parent(aq_inner(context)))).absolute_url()
        else:
            url = context.absolute_url()
        return ["""
        <img src="img/folder_current.png" />
        <a id="currentfolder" href="%s">%s</a>
        """ % (url, translate(self.title, context=context.REQUEST))]


class HomeShortcut(object):
    """Provides shortcut to SiteRoot"""
    title = _(u'Home')

    def render(self, context):
        portal_state = context.restrictedTraverse('@@plone_portal_state')
        return ["""
        <img src="img/home.png" />
        <a id="home" href="%s">%s</a>
        """ % (portal_state.navigation_root_url(),
               translate(self.title, context=context.REQUEST))]
