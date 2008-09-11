from Products.TinyMCE.interfaces.utility import ITinyMCE
from Products.TinyMCE.utility import TinyMCE
from Products.CMFCore.utils import getToolByName

def add_editor(site):
    """ add TinyMCE to 'my preferences' """
    portal_props=getToolByName(site,'portal_properties')
    site_props=getattr(portal_props,'site_properties', None)
    attrname='available_editors'
    if site_props is not None:
        editors=list(site_props.getProperty(attrname))
        if 'TinyMCE' not in editors:
            editors.append('TinyMCE')
        site_props._updateProperty(attrname, editors)

def importVarious(context):
    if context.readDataFile('portal-tinymce.txt') is None:
        return

    site = context.getSite()
    add_editor(site)
