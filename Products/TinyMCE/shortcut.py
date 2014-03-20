"""Shortcuts implementation for Plone"""

from Products.TinyMCE.adapters.interfaces.RootFinder import IRootFinder
from Products.TinyMCE.interfaces.utility import _
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
        root_finder = IRootFinder(context)
        return ["""
        <img src="img/home.png" />
        <a id="home" href="%s">%s</a>
        """ % (root_finder.get_root_url(),
               translate(self.title, context=context.REQUEST))]
