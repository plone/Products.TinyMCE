from Products.CMFPlone.utils import log
from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from zope.component import getUtility
from Products.TinyMCE.interfaces.utility import ITinyMCE
from Products.TinyMCE.transforms.parser import TinyMCEOutput

try:
    from Products.PortalTransforms.z3.interfaces import ITransform
except ImportError:
    ITransform = None
from Products.PortalTransforms.interfaces import itransform

try:
    from celementtree import ElementTree, HTMLTreeBuilder
except ImportError:
    from elementtree import ElementTree, HTMLTreeBuilder    

class html_to_tinymce_output_html:
    """ transform which converts html to tiny output html"""    
    if ITransform is not None:
        implements(ITransform)
    __implements__ = itransform
    __name__ = "html_to_tinymce_output_html"
    inputs = ('text/html',)
    output = "text/x-tinymce-output-html"

    def __init__(self, name=None):
        self.config_metadata = {
            'inputs' : ('list', 'Inputs', 'Input(s) MIME type. Change with care.'),
        }
        if name:
            self.__name__ = name
            
        log("__init__ called")

    def name(self):
        return self.__name__

    def convert(self, orig, data, **kwargs):
        """converts captioned images, and convert uid's to real path's"""
        # Get the context first, if None, return the original text
        context = kwargs.get('context')
        if not context is None:
            # Call the parser and transform the links and images if necessary
            tinymce_utility = getUtility(ITinyMCE)
            parser = TinyMCEOutput(context=context, captioned_images=tinymce_utility.allow_captioned_images)
            parser.feed(orig)
            parser.close()
            data.setData(parser.getResult())
            return data
        data.setData(orig)
        return data
        
def register():
    return html_to_tinymce_output_html()
