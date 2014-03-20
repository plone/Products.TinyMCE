from Acquisition import aq_inner

from plone.app.layout.navigation.root import getNavigationRootObject
from plone.app.layout.navigation.interfaces import INavigationRoot

from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.TinyMCE.adapters.interfaces.RootFinder import IRootFinder

from zope.component import adapts
from zope.interface import implements


class RootFinder(object):
    implements(IRootFinder)
    adapts(IContentish)
    
    def __init__(self, context):
        self.context = aq_inner(context)
        tinymce = getToolByName(self.context, 'portal_tinymce')
        self.use_plone_site_as_root = \
                getattr(tinymce, 'use_plone_site_as_root', False)
    
    def get_root_object(self):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        if self.use_plone_site_as_root:
            return portal
        else:
            return getNavigationRootObject(self.context, portal)
        
    def get_root_url(self):
        return self.get_root_object().absolute_url()
        
    
    def is_root_object(self):
        if self.use_plone_site_as_root:
            return ISiteRoot.providedBy(self.context)
        else:
            return INavigationRoot.providedBy(self.context)


class PloneSiteRootFinder(object):
    implements(IRootFinder)
    adapts(ISiteRoot)
    
    def __init__(self, portal):
        self.portal = aq_inner(portal)
    
    def get_root_object(self):
        return self.portal
    
    def get_root_url(self):
        return self.portal.absolute_url()
    
    def is_root_object(self):
        return True
