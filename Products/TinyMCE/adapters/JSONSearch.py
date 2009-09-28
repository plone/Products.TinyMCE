from zope.interface import implements
from zope.component import adapts
from zope.component import getUtility
try:
    import simplejson as json
except:
    import json

from Products.TinyMCE.interfaces.utility import ITinyMCE
from Products.TinyMCE.adapters.interfaces.JSONSearch import IJSONSearch
from Products.CMFCore.interfaces._content import IContentish, IFolderish
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.CMFPlone.interfaces import INonStructuralFolder
from Products.CMFPlone import utils
from Products.CMFCore.utils import getUtilityByInterfaceName
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner

class JSONSearch(object):
    """Returns a list of search results in JSON"""
    implements(IJSONSearch)

    def __init__(self, context):
        """Constructor"""
        self.context = context

    def getSearchResults(self, filter_portal_types, searchtext):
        """Returns the actual search result"""

        catalog_results = []
        results = {}

        results['parent_url'] = ''
        results['path'] = []

        if searchtext:
            for brain in self.context.portal_catalog.searchResults({'SearchableText':'%s*' % searchtext, 'portal_type':filter_portal_types, 'sort_on':'sortable_title'}):
                catalog_results.append({
                    'id': brain.getId,
                    'uid': brain.UID,
                    'url': brain.getURL(),
                    'portal_type': brain.portal_type,
                    'title' : brain.Title == "" and brain.id or brain.Title,
                    'icon' : brain.getIcon,
                    'is_folderish' : brain.is_folderish
                    })

        # add catalog_results
        results['items'] = catalog_results 
        
        # never allow upload from search results page 
        results['upload_allowed'] = False
        
        # return results in JSON format
        return json.dumps(results)
