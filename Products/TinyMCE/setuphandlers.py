from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import IPropertiesTool
from Products.PortalTransforms.interfaces import IPortalTransformsTool
from Products.MimetypesRegistry.interfaces import IMimetypesRegistryTool

from Products.TinyMCE.interfaces.utility import ITinyMCE
from Products.TinyMCE.utility import TinyMCE
from Products.TinyMCE.mimetypes import text_tinymce_output_html
from Products.TinyMCE.transforms.html_to_tinymce_output_html import html_to_tinymce_output_html
from Products.TinyMCE.transforms.tinymce_output_html_to_html import tinymce_output_html_to_html
from types import InstanceType

from zope.component import getUtility

TINYMCE_OUTPUT_TRANSFORMATION="html_to_tinymce_output_html"

from Products.CMFPlone.utils import log

def add_editor(site):
    """ add TinyMCE to 'my preferences' """
    #portal_props=getToolByName(site,'portal_properties')
    portal_props = getUtility(IPropertiesTool)
    site_props=getattr(portal_props,'site_properties', None)
    attrname='available_editors'
    if not site_props is None:
        editors=list(site_props.getProperty(attrname))
        if 'TinyMCE' not in editors:
            editors.append('TinyMCE')
        site_props._updateProperty(attrname, editors)
        
def register_mimetype(context, mimetype):
    """ register a mimetype with the MIMETypes registry """
    if type(mimetype) != InstanceType:
        mimetype = mimetype()
    mimetypes_registry = getUtility(IMimetypesRegistryTool) 
    mimetypes_registry.register(mimetype)

def unregister_mimeType(context, mimetype):
    """ uregister a mimetype with the MIMETypes registry """
    if type(mimetype) != InstanceType:
        mimetype = mimetype()
    mimetypes_registry = getUtility(IMimetypesRegistryTool)
    mimetypes_registry.unregister(mimetype)
    
def register_transform(context, transform):
    """ register a transform with the portal_transforms tool"""    
    transform_tool = getUtility(IPortalTransformsTool)
    transform = transform()
    transform_tool.registerTransform(transform)
    
def unregister_transform(context, transform):
    """ unregister a transform with the portal_transforms tool"""        
    transform_tool = getUtility(IPortalTransformsTool)
    transform_tool.unregisterTransform(transform)

def register_transform_policy(context, output_mimetype, required_transform):
    """ register a transform policy with the portal_transforms tool"""
    transform_tool = getUtility(IPortalTransformsTool)
    policies = transform_tool.listPolicies()
    # this needs a rewrite, works for now
    install = True
    for policy in policies:
        if policy[0] == output_mimetype:
            install = False
    if install:
        transform_tool.manage_addPolicy(output_mimetype, [required_transform])    

def importVarious(context):
    if context.readDataFile('portal-tinymce.txt') is None:
        return
    site = context.getSite()
    add_editor(site)
    # register text/x-tinymce-output-html mimetype and transformations for captioned images
    register_mimetype(site, text_tinymce_output_html)
    register_transform(site, tinymce_output_html_to_html)
    register_transform(site, html_to_tinymce_output_html)
    
