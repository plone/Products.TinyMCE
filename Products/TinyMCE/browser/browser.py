import httplib

from Acquisition import aq_inner

from zope.interface import implements
from zope.component import getUtility, queryUtility
from zope.component import getMultiAdapter

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from plone.app.layout.viewlets.common import ViewletBase
from Products.TinyMCE.adapters.interfaces.JSONFolderListing import \
     IJSONFolderListing
from Products.TinyMCE.adapters.interfaces.JSONSearch import IJSONSearch
from Products.TinyMCE.adapters.interfaces.JSONDetails import IJSONDetails
from Products.TinyMCE.adapters.interfaces.Upload import IUpload
from Products.TinyMCE.adapters.interfaces.Save import ISave
from Products.TinyMCE.browser.interfaces.browser import ITinyMCEBrowserView
from Products.TinyMCE.browser.interfaces.browser import IATDProxyView
from Products.TinyMCE.interfaces.utility import ITinyMCE


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

    def jsonConfiguration(self, fieldname, script_url=None):
        """Return the configuration in JSON"""
        utility = getToolByName(self.context, 'portal_tinymce')
        return utility.getConfiguration(context=self.context,
                                        field=fieldname,
                                        script_url=script_url,
                                        request=self.request)


class ATDProxyView(object):
    """ Proxy for the 'After the Deadline' spellchecker
    """
    implements(IATDProxyView)

    def checkDocument(self):
        """ Proxy for the AtD service's checkDocument function
            See http://www.afterthedeadline.com/api.slp for more info.
        """
        data = self.request._file.read()

        utility = getUtility(ITinyMCE)
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


class ConfigurationViewlet(ViewletBase):
    """ A viewlet which includes the TinyMCE configuration JavaScript

    This can not be done in the portal_javascript Tool because it needs to be
    relative to the context path.
    """

    index = ViewPageTemplateFile('configuration.pt')

    def show(self):
        tinymce = queryUtility(ITinyMCE, context=self.context)
        if tinymce is None:
            return False
        context = aq_inner(self.context)
        factory = getToolByName(context, 'portal_factory', None)
        if factory is not None and factory.isTemporary(context):
            # Always include TinyMCE on temporary pages
            # These are ment for editing and get false positives
            # with the showEditableBorder-method
            return True
        plone_view = getMultiAdapter((self.context, self.request), name="plone")
        return plone_view.showEditableBorder()
