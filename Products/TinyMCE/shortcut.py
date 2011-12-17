"""Shortcuts implementation for Plone"""

from Products.TinyMCE.interfaces.utility import _
from plone.app.layout.navigation.root import getNavigationRoot
from zope.i18n import translate


class CurrentFolderShortcut(object):
    """Provides shortcut to current folder"""
    title = _(u'Current Folder')

    def render(self, context):
        return ["""
        <img src="img/folder_current.png" />
        <a id="currentfolder" href="%s">%s</a>
        """ % (context.absolute_url(), translate(self.title, context=context.REQUEST))]


class HomeShortcut(object):
    """Provides shortcut to SiteRoot"""
    title = _(u'Home')

    def render(self, context):
        return ["""
        <img src="img/home.png" />
        <a id="home" href="%s">%s</a>
        """ % (getNavigationRoot(context), translate(self.title, context=context.REQUEST))]
