from Products.CMFPlone.utils import log
from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from zope.component import getUtility
from Products.TinyMCE.interfaces.utility import ITinyMCE

try:
    from Products.PortalTransforms.z3.interfaces import ITransform
except ImportError:
    ITransform = None
from Products.PortalTransforms.interfaces import itransform

try:
    from celementtree import ElementTree, HTMLTreeBuilder
except ImportError:
    from elementtree import ElementTree, HTMLTreeBuilder    
from urlparse import urlsplit, urlunsplit
from sgmllib import SGMLParser


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

    def _makeUrlRelative(self, url, base):
        """Make a link relative to base. This method assumes we have already checked that url and base have a common prefix. This is taken from Kupu"""
        sheme, netloc, path, query, fragment = urlsplit(url)
        _, _, basepath, _, _ = urlsplit(base)
    
        baseparts = basepath.split('/')
        pathparts = path.split('/')
    
        basetail = baseparts.pop(-1)
    
        # Remove common elements
        while pathparts and baseparts and baseparts[0]==pathparts[0]:
            baseparts.pop(0)
            pathparts.pop(0)
    
        for i in range(len(baseparts)):
            pathparts.insert(0, '..')
    
        if not pathparts:
            pathparts.insert(0, '.')
        elif pathparts==[basetail]:
            pathparts.pop(0)
        return '/'.join(pathparts)

    def convert(self, orig, data, **kwargs):
        """converts captioned images, and convert uid's to real path's"""
        # TODO : check if elementtree failes
        # TODO : remove span tags at the end
        log("Content zoals hij binnen komt")
        orig = "<span>%s</span>" % orig
        # Get the context first, if None, don't do anything
        context = kwargs.get('context')

        if not context is None:
            log(orig)
            if 1 == 0:
                # disabled for now, rewrite going on with sgmllib                    
                tree = HTMLTreeBuilder.TreeBuilder()
                tree.feed(orig)
                root = tree.close()
                images = root.findall(".//img")
                links = root.findall(".//a")
                for image in images:
                        attributes = {}
                        for (key, value) in image.items():
                            attributes[key] = value
                        src = ""
                        description = ""
                        if attributes.has_key("src"):
                            src = image.get("src")
    
                        if src.find('resolveuid') == 0:
                            parts = src.split("/")
                            # Get the actual uid
                            uid = parts[1]
                            appendix = ""
                            if len(parts) > 2:
                                # There is more than just the uid, save it in appendix
                                appendix = "/" + "/".join(parts[2:])
                            reference_tool = getToolByName(context, 'reference_catalog')
                            image_obj = reference_tool.lookupObject(uid)
                            if image_obj:
                                src = self._makeUrlRelative(image_obj.absolute_url(), context.absolute_url()) + appendix
                                description = image_obj.Description()
                                image.set("src", src)
                        tinymce_utility = getUtility(ITinyMCE)
                        if tinymce_utility.allow_captioned_images and image.get("class").find('captioned') != -1:
                            # We have captioned images, and we need to convert them 
                            classes = ""       
                            if attributes.has_key("class"):
                                classes = image.get("class")
                            width_style = ""    
                            if attributes.has_key("width"):
                                width_style="style=\"width:%spx;\" " % image.get("width")
                            image_attributes = ""
                            image_attributes = image_attributes.join(["%s %s=\"%s\"" % (image_attributes, key, value) for (key, value) in attributes.items() if not key in ["class", "src"]])
                            captioned_html = """
                                                <dl %sclass="%s"> 
                                                <dt %s>
                                                    <img %s src="%s"/>
                                                </dt>
                                                <dd class="image-caption">
                                                    %s
                                                </dd>
                                                </dl>""" % (width_style, classes, width_style, image_attributes, src ,description)
                            log("jow")
                            log(captioned_html)
                            dl = ElementTree.fromstring(captioned_html)
                            image.clear()
                            image.tag = "dl"
                            image[:] = [dl]
                
                for link in links:
                    if link.get("href"):
                        href = link.get("href")
                        if href.find('resolveuid') == 0:
                            parts = href.split("/")
                            # Get the actual uid
                            uid = parts[1]
                            appendix = ""
                            if len(parts) > 2:
                                # There is more than just the uid, save it in appendix
                                appendix = "/".join(parts[2:])
                            reference_tool = getToolByName(context, 'reference_catalog')
                            ref_obj = reference_tool.lookupObject(uid)
                            if ref_obj:
                                href = self._makeUrlRelative(ref_obj.absolute_url(), context.absolute_url()) + appendix
                                link.set("href", href)                    
                        
                converted_html = ElementTree.tostring(root)
                log("content na de transform")
                log(converted_html)
                #print(orig)
                #print("===")
                #print(converted_html)
                # TODO : remove <span!>
            else:
                pass            
            data.setData(orig)
            return data        

def register():
    return html_to_tinymce_output_html()
