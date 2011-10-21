# BBB for what ???

from Products.MimetypesRegistry.MimeTypeItem import MimeTypeItem


class text_tinymce_output_html(MimeTypeItem):
    __name__ = "TinyMCE Output HTML"
    mimetypes = ('text/x-tinymce-output-html',)
    binary = 0
