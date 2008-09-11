from zope.interface import Interface

class IJSONFolderListing(Interface):
	"""Returns a folderish like listing in JSON"""

	def __init__(self, context):
		"""Constructor"""
		
	def getBreadcrums(self):
		"""Get breadcrums"""
	
	def getListing(self, filter_meta_types):
		"""Returns the actual listing"""

	def getInfoFromBrain(self, brain):
	    """
		Gets information from a brain
		id, url, portal_type, title, icon, is_folderish
	    """
	