import httplib
try:
    import simplejson as json
    json  # Pyflakes
except ImportError:
    import json

from Acquisition import aq_inner

from zope.interface import implements

from Products.Five.browser import BrowserView

from Products.CMFCore.utils import getToolByName

from Products.TinyMCE.adapters.interfaces.JSONFolderListing import \
     IJSONFolderListing
from Products.TinyMCE.adapters.interfaces.JSONSearch import IJSONSearch
from Products.TinyMCE.adapters.interfaces.JSONDetails import IJSONDetails
from Products.TinyMCE.adapters.interfaces.Upload import IUpload
from Products.TinyMCE.adapters.interfaces.Save import ISave
from Products.TinyMCE.browser.interfaces.browser import ITinyMCEBrowserView
from Products.TinyMCE.browser.interfaces.browser import IATDProxyView


class TinyMCEBrowserView(BrowserView):
    """TinyMCE Browser View"""
    implements(ITinyMCEBrowserView)

    def upload(self):
        """Upload a file to the zodb"""

        context = IUpload(self.context)
        return context.upload()

    def save(self, text, fieldname):
        """Saves the specified richedit field"""

        object = ISave(self.context)
        return object.save(text, fieldname)

    def setDescription(self, description):
        """Sets the description of an inserted image"""

        if isinstance(description, str):
            description = description.decode('utf-8')
        object = IUpload(self.context)
        return object.setDescription(description)

    def jsonLinkableFolderListing(self, rooted, document_base_url):
        """Returns the folderlisting of linkable objects in JSON"""

        utility = getToolByName(aq_inner(self.context), 'portal_tinymce')
        linkable_portal_types = utility.linkable.split('\n')

        object = IJSONFolderListing(self.context, None)
        if object is None:
            return ''
        results = object.getListing(
            linkable_portal_types,
            rooted,
            document_base_url,
            'File',
            utility.imageobjects.split('\n'),
        )
        return results

    def jsonImageFolderListing(self, rooted, document_base_url):
        """Returns the folderlisting of image objects in JSON"""

        utility = getToolByName(aq_inner(self.context), 'portal_tinymce')
        image_portal_types = utility.imageobjects.split('\n')
        image_portal_types.extend(utility.containsobjects.split('\n'))

        object = IJSONFolderListing(self.context, None)
        if object is None:
            return ''
        results = object.getListing(
            image_portal_types,
            rooted,
            document_base_url,
            'Image',
            utility.imageobjects.split('\n'),
        )
        return results

    def jsonLinkableSearch(self, searchtext):
        """Returns the search results of linkable objects in JSON"""

        utility = getToolByName(aq_inner(self.context), 'portal_tinymce')
        linkable_portal_types = utility.linkable.split('\n')
        linkable_portal_types.extend(utility.containsobjects.split('\n'))

        object = IJSONSearch(self.context, None)
        if object is None:
            return ''
        results = object.getSearchResults(linkable_portal_types, searchtext)
        return results

    def jsonImageSearch(self, searchtext):
        """Returns the search results of image objects in JSON"""

        utility = getToolByName(aq_inner(self.context), 'portal_tinymce')
        image_portal_types = utility.imageobjects.split('\n')
        image_portal_types.extend(utility.containsobjects.split('\n'))

        object = IJSONSearch(self.context, None)
        if object is None:
            return ''
        results = object.getSearchResults(image_portal_types, searchtext)
        return results

    def jsonDetails(self):
        """Returns the details of an object in JSON"""

        object = IJSONDetails(self.context, None)
        if object is None:
            return ''
        return object.getDetails()

    def jsonConfiguration(self, field):
        """Return the configuration in JSON"""

        utility = getToolByName(aq_inner(self.context), 'portal_tinymce')
        config = utility.getConfiguration(context=self.context,
                                          field=field,
                                          request=self.request)
        config['relative_urls'] = False
        return json.dumps(config)


class ATDProxyView(object):
    """ Proxy for the 'After the Deadline' spellchecker
    """
    implements(IATDProxyView)

    def checkDocument(self):
        """ Proxy for the AtD service's checkDocument function
            See http://www.afterthedeadline.com/api.slp for more info.
        """
        data = self.request._file.read()

        utility = getToolByName(self.context, 'portal_tinymce')
        service_url = utility.libraries_atd_service_url
        service = httplib.HTTPConnection(service_url)

        service.request("POST", "/checkDocument", data)
        response = service.getresponse()
        service.close()

        if response.status != httplib.OK:
            raise Exception('Unexpected response code from AtD service %d' %
                            response.status)

        self.request.RESPONSE.setHeader('content-type',
                                        'text/xml;charset=utf-8')
        respxml = response.read()
        xml = respxml.strip().replace("\r", '').replace("\n", '').replace(
            '>  ', '>')
        return xml
