# BBB

from Products.MimetypesRegistry.interfaces import IClassifier
from Products.MimetypesRegistry.MimeTypeItem import MimeTypeItem
from Products.MimetypesRegistry.common import MimeTypeException
from Products.MimetypesRegistry.interfaces import IMimetype
from zope.interface import implements
from types import InstanceType


class text_tinymce_output_html(MimeTypeItem):
    __name__ = "TinyMCE Output HTML"
    mimetypes = ('text/x-tinymce-output-html',)
    binary = 0
