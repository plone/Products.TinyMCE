# BBB

from zope.component import getAdapters
from zope.interface import implements
from zope.app.component.hooks import getSite

try:
    try:
        from Products.PortalTransforms.interfaces import ITransform
    except ImportError:
        from Products.PortalTransforms.z3.interfaces import ITransform
except ImportError:
    ITransform = None
from Products.PortalTransforms.interfaces import itransform

from plone.outputfilters.interfaces import IFilter
from plone.outputfilters import apply_filters


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
            'inputs': ('list', 'Inputs', 'Input(s) MIME type. Change with care.'),
        }
        if name:
            self.__name__ = name

    def name(self):
        return self.__name__

    def convert(self, orig, data, **kwargs):
        """apply plone.outputfilters filters"""
        context = kwargs.get('context')
        request = getattr(getSite(), 'REQUEST', None)
        filters = [f for _, f in getAdapters((context, request), IFilter)]

        res = apply_filters(filters, orig)
        data.setData(res)
        return data


# This needs to be here to avoid breaking existing instances
def register():
    return html_to_tinymce_output_html()
