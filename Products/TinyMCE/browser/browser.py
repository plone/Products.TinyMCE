from zope.interface import implements
from zope.component import getUtility
from Products.Five.browser import BrowserView
from Acquisition import aq_inner

from Products.TinyMCE.adapters.interfaces.JSONFolderListing import \
     IJSONFolderListing
from Products.TinyMCE.adapters.interfaces.JSONSearch import IJSONSearch
from Products.TinyMCE.adapters.interfaces.JSONDetails import IJSONDetails
from Products.TinyMCE.adapters.interfaces.Upload import IUpload
from Products.TinyMCE.adapters.interfaces.Save import ISave
from Products.TinyMCE.browser.interfaces.browser import ITinyMCEBrowserView
from Products.TinyMCE.interfaces.utility import ITinyMCE


class TinyMCEBrowserView(BrowserView):
    """TinyMCE Browser View"""
    implements(ITinyMCEBrowserView)

    def upload(self):
        """Upload a file to the zodb"""

        context = aq_inner(self.context)
        object = IUpload(context)
        return object.upload()

    def save(self, text, fieldname):
        """Saves the specified richedit field"""

        context = aq_inner(self.context)
        object = ISave(context)
        return object.save(text, fieldname)

    def jsonLinkableFolderListing(self, rooted, document_base_url):
        """Returns the folderlisting of linkable objects in JSON"""

        utility = getUtility(ITinyMCE)
        linkable_portal_types = utility.linkable.split('\n')

        context = aq_inner(self.context)
        object = IJSONFolderListing(context)
        results = object.getListing(linkable_portal_types, rooted,
                                    document_base_url, 'File')
        return results

    def jsonImageFolderListing(self, rooted, document_base_url):
        """Returns the folderlisting of image objects in JSON"""

        utility = getUtility(ITinyMCE)
        image_portal_types = utility.imageobjects.split('\n')
        image_portal_types.extend(utility.containsobjects.split('\n'))

        context = aq_inner(self.context)
        object = IJSONFolderListing(context)
        results = object.getListing(image_portal_types, rooted,
                                    document_base_url, 'Image')
        return results

    def jsonLinkableSearch(self, searchtext):
        """Returns the search results of linkable objects in JSON"""

        utility = getUtility(ITinyMCE)
        linkable_portal_types = utility.linkable.split('\n')
        linkable_portal_types.extend(utility.containsobjects.split('\n'))

        context = aq_inner(self.context)
        object = IJSONSearch(context)
        results = object.getSearchResults(linkable_portal_types, searchtext)
        return results

    def jsonImageSearch(self, searchtext):
        """Returns the search results of image objects in JSON"""

        utility = getUtility(ITinyMCE)
        image_portal_types = utility.imageobjects.split('\n')
        image_portal_types.extend(utility.containsobjects.split('\n'))

        context = aq_inner(self.context)
        object = IJSONSearch(context)
        results = object.getSearchResults(image_portal_types, searchtext)
        return results

    def jsonDetails(self):
        """Returns the details of an object in JSON"""

        context = aq_inner(self.context)
        object = IJSONDetails(context)
        return object.getDetails()

    def jsonConfiguration(self, fieldname):
        """Return the configuration in JSON"""
        utility = getUtility(ITinyMCE)
        context = aq_inner(self.context)
        return utility.getConfiguration(context=context,
                                        field=fieldname,
                                        request=self.request)
