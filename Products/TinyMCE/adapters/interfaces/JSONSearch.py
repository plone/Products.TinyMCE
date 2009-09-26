from zope.interface import Interface

class IJSONSearch(Interface):
    """Returns a list of search results in JSON"""

    def __init__(self, context):
        """Constructor"""

    def getSearchResults(self, filter_portal_types, searchtext):
        """Returns the actual search results"""
