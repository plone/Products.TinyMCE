try:
    import simplejson as json
    json   # pyflakes
except ImportError:
    import json

from zope.interface import implements
from zope.component import getUtility
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.app.layout.navigation.root import getNavigationRootObject
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFCore.interfaces._content import IFolderish
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner
from Acquisition import aq_parent

from Products.TinyMCE.adapters.interfaces.JSONFolderListing import IJSONFolderListing


class JSONFolderListing(object):
    """Returns a folderish like listing in JSON"""
    implements(IJSONFolderListing)

    root_icon = "img/home.png"
    folder_icon = "img/folder.png"
    listing_base_query = {}

    def __init__(self, context):
        """Constructor"""
        self.context = context

    def getBreadcrumbs(self, path=None):
        """Get breadcrumbs"""
        result = []

        portal_state = self.context.restrictedTraverse('@@plone_portal_state')
        root = getNavigationRootObject(self.context, portal_state.portal())
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
                'title': translate(MessageFactory('plone')('Home'), context=self.context.REQUEST),
                'url': root_url,
                'icon': '<img src="%s" width="16" height="16" />' % icon,
            })

        for i in range(len(relative)):
            now = relative[:i + 1]
            obj = aq_inner(root.restrictedTraverse(now))

            if IFolderish.providedBy(obj):
                if not now[-1] == 'talkback':
                    result.append({
                        'title': obj.title_or_id(),
                        'url': root_url + '/' + '/'.join(now),
                        'icon': '<img src="%s" width="16" height="16" />' % self.folder_icon,
                    })
        return result

    def getListing(self, filter_portal_types, rooted, document_base_url, upload_type=None, image_types=None):
        """Returns the actual listing"""
        catalog_results = []
        results = {}
        image_types = image_types or []

        object = aq_inner(self.context)
        portal_catalog = getToolByName(object, 'portal_catalog')
        normalizer = getUtility(IIDNormalizer)

        # check if object is a folderish object, if not, get it's parent.
        if not IFolderish.providedBy(object):
            object = aq_parent(object)

        if INavigationRoot.providedBy(object) or (rooted == "True" and document_base_url[:-1] == object.absolute_url()):
            results['parent_url'] = ''
        else:
            results['parent_url'] = aq_parent(object).absolute_url()

        if rooted == "True":
            results['path'] = self.getBreadcrumbs(results['parent_url'])
        else:
            # get all items from siteroot to context (title and url)
            results['path'] = self.getBreadcrumbs()

        plone_layout = self.context.restrictedTraverse('@@plone_layout', None)
        if plone_layout is None:
            # Plone 3
            plone_view = self.context.restrictedTraverse('@@plone')
            getIcon = lambda brain: plone_view.getIcon(brain).html_tag()
        else:
            # Plone >= 4
            getIcon = lambda brain: plone_layout.getIcon(brain)()

        # get all portal types and get information from brains
        path = '/'.join(object.getPhysicalPath())
        query = self.listing_base_query.copy()
        query.update({'portal_type': filter_portal_types,
                      'sort_on': 'getObjPositionInParent',
                      'path': {'query': path, 'depth': 1}})
        for brain in portal_catalog(**query):
            catalog_results.append({
                'id': brain.getId,
                'uid': brain.UID or None,  # Maybe Missing.Value
                'url': brain.getURL(),
                'review_state': brain.review_state or None,  # Maybe Missing.Value
                'portal_type': brain.portal_type,
                'normalized_type': normalizer.normalize(brain.portal_type),
                'title': brain.Title == "" and brain.id or brain.Title,
                'icon': getIcon(brain),
                'description': unicode(brain.Description, 'utf-8', 'ignore'),
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
