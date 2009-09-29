from Products.CMFPlone.utils import log
from zope.interface import implements

try:
    try:
        from Products.PortalTransforms.interfaces import ITransform
    except ImportError:
        from Products.PortalTransforms.z3.interfaces import ITransform
except ImportError:
    ITransform = None
from Products.PortalTransforms.interfaces import itransform

class tinymce_output_html_to_html:
    """ transform which converts tinymce output html to html"""
    if ITransform is not None:
        implements(ITransform)
    __implements__ = itransform
    __name__ = "tinymce_output_html_to_html"
    inputs = ('text/x-tinymce-output-html',)
    output = "text/html"

    def __init__(self, name=None):
        self.config_metadata = {
            'inputs' : ('list', 'Inputs', 'Input(s) MIME type. Change with care.'),
        }
        if name:
            self.__name__ = name

    def name(self):
        return self.__name__

    def convert(self, orig, data, **kwargs):
        # we actually don't do anything in this transform, it is needed to get back in the transformation policy chain
        text = orig
        data.setData(text)
        return data

# This needs to be here to avoid breaking existing instances
def register():
    return tinymce_output_html_to_html()
