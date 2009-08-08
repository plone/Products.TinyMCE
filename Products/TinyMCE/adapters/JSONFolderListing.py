from zope.interface import implements
from zope.component import adapts
from zope.component import getUtility
from z3c.json import interfaces
from z3c.json import testing

from Products.TinyMCE.interfaces.utility import ITinyMCE
from Products.TinyMCE.adapters.interfaces.JSONFolderListing import IJSONFolderListing
from Products.CMFCore.interfaces._content import IContentish, IFolderish
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.CMFPlone.interfaces import INonStructuralFolder
from Products.CMFPlone import utils
from Products.CMFCore.utils import getUtilityByInterfaceName
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner

class JSONFolderListing(object):
    """Returns a folderish like listing in JSON"""
    implements(IJSONFolderListing)
    #adapts(IContentish, IPloneSiteRoot)

    def __init__(self, context):
        """Constructor"""
        self.context = context

    def getBreadcrums(self):
        """Get breadcrums"""
        #TODO: getToolByName is deprecated
        ptool = getUtilityByInterfaceName('Products.CMFCore.interfaces.IPropertiesTool')
        utool = getToolByName(self.context, 'portal_url')
        portal_url = utool()
        result = []

        # SiteRoot
        result.append({'title':ptool.title(),'url':portal_url})

        relative = utool.getRelativeContentPath(self.context)
        portal = utool.getPortalObject()

        for i in range(len(relative)):
            now = relative[ :i+1 ]
            obj = aq_inner(portal.restrictedTraverse(now))

            if IFolderish.providedBy(obj):
                if not now[-1] == 'talkback':
                    result.append({'title':obj.Title(),'url':portal_url + '/' + '/'.join(now)})
        return result

    def getInfoFromBrain(self, brain):
        """Gets information from a brain id, url, portal_type, title, icon, is_folderish"""

        id = brain.getId
        uid = brain.UID
        url = brain.getURL()
        portal_type = brain.portal_type
        title = brain.Title
        icon = brain.getIcon
        is_folderish = brain.is_folderish

        return {
        'id': id,
        'uid': uid,
        'url': url,
        'portal_type': portal_type,
        'title' : title,
        'icon' : icon,
        'is_folderish' : is_folderish
        }

    def getListing(self, filter_portal_types):
        """Returns the actual listing"""

        catalog_results = []
        results = {}

        object = aq_inner(self.context)

        if IPloneSiteRoot.providedBy(object):
            results['parent_url'] = ''
        else:
            results['parent_url'] = object.getParentNode().absolute_url()

        # get all items from siteroot to context (title and url)
        results['path'] = self.getBreadcrums()

        # check if object is a folderish object, if not, get it's parent.
        if not IFolderish.providedBy(object):
            object = object.getParentNode()
        
        # get all portal types and get information from brains
        for brain in object.getFolderContents({'portal_type':filter_portal_types, 'sort_on':'sortable_title'}):
            catalog_results.append(self.getInfoFromBrain(brain))

        # add catalog_ressults
        results['items'] = catalog_results 

        # return results in JSON format
        testing.setUpJSONConverter()
        jsonWriter = getUtility(interfaces.IJSONWriter)
        return jsonWriter.write(results)
