"""Shortcuts implementation for Plone"""

from Products.TinyMCE.interfaces.utility import _
from plone.app.layout.navigation.root import getNavigationRoot


class CurrentFolderShortcut(object):
    """Provides shortcut to current folder"""
    title = _(u'Current Folder')

    def render(self, context):
        return ["""
        <img src="img/folder_current.png" />
        <a id="currentfolder" href="%s">%s</a>
        """ % (context.absolute_url(), self.title)]


class HomeShortcut(object):
    """Provides shortcut to SiteRoot"""
    title = _(u'Home')

    def render(self, context):
        return ["""
        <img src="img/home.png" />
        <a id="home" href="%s">%s</a>
        """ % (getNavigationRoot(context), self.title)]
