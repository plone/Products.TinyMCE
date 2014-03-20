from zope.interface import Interface


class IRootFinder(Interface):
    """ Adapts a content object to help find the root content object for the
        editor. 
    """
    
    def get_root_object(self):
        """ The root object of the editor """
        
    def get_root_url(self, request):
        """ The URL of the root object """
        
    def is_root_object(self):
        """ Is the adapted context object the root object of the editor """
