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

import transaction

def add_editor(site):
    """ add TinyMCE to 'my preferences' """
    portal_props = getUtility(IPropertiesTool)
    site_props=getattr(portal_props,'site_properties', None)
    attrname='available_editors'
    if not site_props is None:
        editors=list(site_props.getProperty(attrname))
        if 'TinyMCE' not in editors:
            editors.append('TinyMCE')
        site_props._updateProperty(attrname, editors)

def remove_editor(site):
    """ Remove TinyMCE from 'my preferences' """
    portal_props = getUtility(IPropertiesTool)
    site_props=getattr(portal_props,'site_properties', None)
    attrname='available_editors'
    if not site_props is None:
        editors=list(site_props.getProperty(attrname))
        editors=[x for x in editors if x != 'TinyMCE']
        site_props._updateProperty(attrname, editors)

def register_mimetype(context, mimetype):
    """ register a mimetype with the MIMETypes registry """
    if type(mimetype) != InstanceType:
        mimetype = mimetype()
    mimetypes_registry = getUtility(IMimetypesRegistryTool)
    mimetypes_registry.register(mimetype)

def unregister_mimetype(context, mimetype):
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
    # XXX How to check if transform exists?
    if hasattr(transform_tool, transform):
        transform_tool.unregisterTransform(transform)

def register_transform_policy(context, output_mimetype, required_transform):
    """ register a transform policy with the portal_transforms tool"""
    transform_tool = getUtility(IPortalTransformsTool)
    unregister_transform_policy(context, output_mimetype)
    transform_tool.manage_addPolicy(output_mimetype, [required_transform])

def unregister_transform_policy(context, output_mimetype):
    """ unregister a transform policy with the portal_transforms tool"""
    transform_tool = getUtility(IPortalTransformsTool)
    policies = [mimetype for (mimetype, required) in transform_tool.listPolicies() if mimetype == output_mimetype]
    if policies:
        # There is a policy, remove it!
        transform_tool.manage_delPolicies([output_mimetype])

def install_mimetype_and_transforms(context):
    """ register text/x-tinymce-output-html mimetype and transformations for captioned images """
    register_mimetype(context, text_tinymce_output_html)
    register_transform(context, tinymce_output_html_to_html)
    register_transform(context, html_to_tinymce_output_html)
    register_transform_policy(context, "text/x-html-safe", "html_to_tinymce_output_html")

def uninstall_mimetype_and_transforms(context):
    """ unregister text/x-tinymce-output-html mimetype and transformations for captioned images """
    unregister_transform(context, "tinymce_output_html_to_html")
    unregister_transform(context, "html_to_tinymce_output_html")
    unregister_mimetype(context, text_tinymce_output_html)
    unregister_transform_policy(context, "text/x-html-safe")

def fix_styles_plone3(context):
    portal_tinymce = getToolByName(context, 'portal_tinymce')
    portal_migration = getToolByName(context, 'portal_migration')

    use_tiny_mce_plone3_styles = False
    if hasattr(portal_migration, 'getInstanceVersionTuple'):
        major_version = portal_migration.getInstanceVersionTuple()[0]
        if major_version == 3:
            use_tiny_mce_plone3_styles = True
    portal_tinymce.use_tiny_mce_plone3_styles = use_tiny_mce_plone3_styles

def importVarious(context):
    if context.readDataFile('portal-tinymce.txt') is None:
        return
    site = context.getSite()
    add_editor(site)
    fix_styles_plone3(site)

def unregisterUtility(context):
    my_utility = getUtility(ITinyMCE)
    context.getSiteManager().unregisterUtility(my_utility, ITinyMCE)
    del my_utility

    transaction.commit()