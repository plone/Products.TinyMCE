from Products.CMFPlone.utils import log
from zope.interface import implements
try:
    from Products.PortalTransforms.z3.interfaces import ITransform
except ImportError:
    ITransform = None
from Products.PortalTransforms.interfaces import itransform

try:
    from celementtree import ElementTree
except ImportError:
    from elementtree import ElementTree

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
        """converts captioned images, and convert uid's to real path's"""
        root = ElementTree.fromstring(orig)
        images = root.findall(".//img")
        for image in images:
            if image.get("class").find('captioned') != -1:
                # We have captioned images, let's convert them
                src = image.get('src')
                classes = image.get("class")
                width = image.get("width")
                
                if src.find('resolveuid') == 0:
                    # search uid and put the actual path back
                    # TODO: What to do when not found?
                    src = src
                    description = "This is my description"
                else:
                    description = "This is my description"

                captioned_html = """
                                    <dl class="%s" style="width:%spx;"> 
                                    <dt style="width:%spx;">
                                        <img src="%s" width="%s" />
                                    </dt>
                                    <dd class="image-caption">
                                        %s
                                    </dd>
                                    </dl>""" % (classes, width, width, src, width, description)
                dl = ElementTree.fromstring(captioned_html)
                image.clear()
                image.tag = "dl"
                image[:] = [dl]
        converted_html = ElementTree.tostring(root)
        log(orig)
        log("===")
        log(converted_html)
        data.setData(converted_html)
        return data        

def register():
    return html_to_tinymce_output_html()