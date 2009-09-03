from zope.interface import Interface

class IJSONSearch(Interface):
    """Returns a list of search results in JSON"""

    def __init__(self, context):
        """Constructor"""

    def getSearchResults(self, filter_portal_types, searchtext):
        """Returns the actual search results"""

    def getInfoFromBrain(self, brain):
        """
        Gets information from a brain
        id, url, portal_type, title, icon, is_folderish
        """
