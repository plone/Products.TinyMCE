from Products.CMFPlone.utils import log
from zope.interface import implements
try:
    from Products.PortalTransforms.z3.interfaces import ITransform
except ImportError:
    ITransform = None
from Products.PortalTransforms.interfaces import itransform

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

    def name(self):
        return self.__name__

    def convert(self, orig, data, **kwargs):
        # TODO : add real caption transforms here
        data.setData(orig)
        return data        

def register():
    return html_to_tinymce_output_html()