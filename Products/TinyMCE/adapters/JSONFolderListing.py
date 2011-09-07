try:
    import json
    json   # pyflakes
except ImportError:
    import simplejson as json

from zope.interface import implements
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFCore.interfaces._content import IFolderish
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner

from Products.TinyMCE.adapters.interfaces.JSONFolderListing import IJSONFolderListing


class JSONFolderListing(object):
    """Returns a folderish like listing in JSON"""
    implements(IJSONFolderListing)

    root_icon = "img/home.png"
    folder_icon = "img/folder.png"
    picture_icon = "img/picture.png"

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
            path = path.replace(root_url, '', 1).strip('/')
            root = aq_inner(root.restrictedTraverse(path))

        relative = aq_inner(self.context).getPhysicalPath()[len(root.getPhysicalPath()):]
        if path is None:
            # Add siteroot
            if IPloneSiteRoot.providedBy(root):
                icon = self.root_icon
            else:
                icon = self.folder_icon
            result.append({
                'title': root.title_or_id(),
                'url': '/'.join(root.getPhysicalPath()),
                'icon': icon,
            })

        for i in range(len(relative)):
            now = relative[:i + 1]
            obj = aq_inner(root.restrictedTraverse(now))

            if IFolderish.providedBy(obj):
                if not now[-1] == 'talkback':
                    result.append({
                        'title': obj.title_or_id(),
                        'url': root_url + '/' + '/'.join(now),
                        'icon': self.folder_icon,
                    })
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
        for brain in portal_catalog(portal_type=filter_portal_types, sort_on='getObjPositionInParent', path={'query': path, 'depth': 1}):
            if brain.is_folderish:
                icon = self.folder_icon
            else:
                icon = self.picture_icon

            catalog_results.append({
                'id': brain.getId,
                'uid': brain.UID or None,  # Maybe Missing.Value
                'url': brain.getURL(),
                'portal_type': brain.portal_type,
                'normalized_type': normalizer.normalize(brain.portal_type),
                'title': brain.Title == "" and brain.id or brain.Title,
                'icon': icon,
                'description': brain.Description,
                'is_folderish': brain.is_folderish,
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
        self.context.REQUEST.response.setHeader("Content-type", "application/json")
        return json.dumps(results)
