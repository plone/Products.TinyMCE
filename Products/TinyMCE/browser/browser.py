from zope.interface import implements
from zope.component import getUtility
from Products.Five.browser import BrowserView
from Acquisition import aq_inner

from Products.TinyMCE.adapters.interfaces.JSONFolderListing import IJSONFolderListing;
from Products.TinyMCE.adapters.interfaces.JSONDetails import IJSONDetails;
from Products.TinyMCE.adapters.interfaces.Upload import IUpload;
from Products.TinyMCE.browser.interfaces.browser import ITinyMCEBrowserView
from Products.TinyMCE.interfaces.utility import ITinyMCE

class TinyMCEBrowserView(BrowserView):
	"""TinyMCE Browser View"""
	implements(ITinyMCEBrowserView)

	def upload(self):
		"""Upload a file to the zodb"""

		context = aq_inner(self.context)
		object = IUpload(self.context)
		return object.upload()
	
	def jsonLinkableFolderListing(self):
		"""Returns the folderlisting of linkable objects in JSON"""

		utility = getUtility(ITinyMCE)
		linkable_meta_types = utility.linkable.split('\n')

		context = aq_inner(self.context)
		object = IJSONFolderListing(self.context)
		return object.getListing(linkable_meta_types)
	
	def jsonImageFolderListing(self):
		"""Returns the folderlisting of image objects in JSON"""

		utility = getUtility(ITinyMCE)
		image_meta_types = utility.imageobjects.split('\n')
		image_meta_types.extend(utility.containsobjects.split('\n'))

		context = aq_inner(self.context)
		object = IJSONFolderListing(self.context)
		return object.getListing(image_meta_types)

	def jsonDetails(self):
		"""Returns the details of an object in JSON"""
	
		context = aq_inner(self.context)
		object = IJSONDetails(self.context)
		return object.getDetails()
