from zope.interface import Interface

class ITinyMCEBrowserView(Interface):
    """TinyMCE Browser View"""

    def upload(self):
        """Upload a file to the zodb"""

    def save(self, text, fieldname):
        """Saves the specified richedit field"""

    def jsonLinkableFolderListing(self):
        """Returns the folderlisting of linkable objects in JSON"""

    def jsonImageFolderListing(self):
        """Returns the folderlisting of image objects in JSON"""

    def jsonLinkableSearch(self):
        """Returns the search results of linkable objects in JSON"""

    def jsonImageSearch(self):
        """Returns the search results of image objects in JSON"""

    def jsonDetails(self):
        """Returns the details of an object in JSON"""
