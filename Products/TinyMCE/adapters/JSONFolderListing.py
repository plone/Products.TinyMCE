from zope.interface import implements
from zope.component import getUtility

try:
    import json
except ImportError:
    import simplejson as json

from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.TinyMCE.adapters.interfaces.JSONFolderListing import IJSONFolderListing
from Products.CMFCore.interfaces._content import IFolderish
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner

class JSONFolderListing(object):
    """Returns a folderish like listing in JSON"""
    implements(IJSONFolderListing)

    def __init__(self, context):
        """Constructor"""
        self.context = context

    def getBreadcrumbs(self, path=None):
        """Get breadcrumbs"""
        result = []

        root_url = getNavigationRoot(self.context)
        root = aq_inner(self.context.restrictedTraverse(root_url))
        root_url = root.absolute_url()

        if path is not None:
            root_abs_url = root.absolute_url()
            path = path.replace(root_abs_url, '', 1)
            path = path.strip('/')
            root = aq_inner(root.restrictedTraverse(path))

        relative = aq_inner(self.context).getPhysicalPath()[len(root.getPhysicalPath()):]
        if path is None:
            # Add siteroot
            result.append({'title':root.title_or_id(),'url':'/'.join(root.getPhysicalPath())})

        for i in range(len(relative)):
            now = relative[ :i+1 ]
            obj = aq_inner(root.restrictedTraverse(now))

            if IFolderish.providedBy(obj):
                if not now[-1] == 'talkback':
                    result.append({'title':obj.title_or_id(),'url':root_url + '/' + '/'.join(now)})
        return result


    def getListing(self, filter_portal_types, rooted, document_base_url, upload_type=None):
        """Returns the actual listing"""

        catalog_results = []
        results = {}

        object = aq_inner(self.context)
        portal_catalog = getToolByName(object, 'portal_catalog')
        normalizer = getUtility(IIDNormalizer)

        # check if object is a folderish object, if not, get it's parent.
        if not IFolderish.providedBy(object):
            object = object.getParentNode()

        if INavigationRoot.providedBy(object) or (rooted == "True" and document_base_url[:-1] == object.absolute_url()):
            results['parent_url'] = ''
        else:
            results['parent_url'] = object.getParentNode().absolute_url()

        if rooted == "True":
            results['path'] = self.getBreadcrumbs(results['parent_url'])
        else:
            # get all items from siteroot to context (title and url)
            results['path'] = self.getBreadcrumbs()
        
        # get all portal types and get information from brains
        path = '/'.join(object.getPhysicalPath())
        for brain in portal_catalog(portal_type=filter_portal_types, sort_on='getObjPositionInParent', path={'query': path, 'depth':1}):
            catalog_results.append({
                'id': brain.getId,
                'uid': brain.UID or None, # Maybe Missing.Value
                'url': brain.getURL(),
                'portal_type': brain.portal_type,
                'normalized_type': normalizer.normalize(brain.portal_type),
                'title' : brain.Title == "" and brain.id or brain.Title,
                'icon' : brain.getIcon,
                'is_folderish' : brain.is_folderish
                })

        # add catalog_ressults
        results['items'] = catalog_results 
        
        # decide whether to show the upload new button
        results['upload_allowed'] = False
        if upload_type:
            portal_types = getToolByName(object, 'portal_types')
            fti = getattr(portal_types, upload_type, None)
            if fti is not None:
                results['upload_allowed'] = fti.isConstructionAllowed(object) 
        
        # return results in JSON format
        return json.dumps(results)
