from Products.MimetypesRegistry.interfaces import IClassifier
from Products.MimetypesRegistry.MimeTypeItem import MimeTypeItem
from Products.MimetypesRegistry.common import MimeTypeException

from types import InstanceType

class text_tinymce_output_html(MimeTypeItem):

    __implements__ = MimeTypeItem.__implements__
    __name__   = "TinyMCE Output HTML"
    mimetypes  = ('text/x-tinymce-output-html',)
    extensions = ('html',)
    binary     = 0
