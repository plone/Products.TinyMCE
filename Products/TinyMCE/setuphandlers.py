from Products.CMFCore.interfaces import IPropertiesTool
from Products.TinyMCE.interfaces.utility import ITinyMCE

from plone.outputfilters.setuphandlers import unregister_mimetype
from plone.outputfilters.setuphandlers import unregister_transform
from plone.outputfilters.setuphandlers import unregister_transform_policy
from plone.outputfilters.setuphandlers import register_transform_policy

from zope.component import getUtility
from zope.deferredimport import deprecatedFrom

import transaction


def add_editor(site):
    """ add TinyMCE to 'my preferences' """
    portal_props = getUtility(IPropertiesTool)
    site_props = getattr(portal_props, 'site_properties', None)
    attrname = 'available_editors'
    if not site_props is None:
        editors = list(site_props.getProperty(attrname))
        if 'TinyMCE' not in editors:
            editors.append('TinyMCE')
        site_props._updateProperty(attrname, editors)


def remove_editor(site):
    """ Remove TinyMCE from 'my preferences' """
    portal_props = getUtility(IPropertiesTool)
    site_props = getattr(portal_props, 'site_properties', None)
    attrname = 'available_editors'
    if not site_props is None:
        editors = list(site_props.getProperty(attrname))
        editors = [x for x in editors if x != 'TinyMCE']
        site_props._updateProperty(attrname, editors)


def uninstall_mimetype_and_transforms(context):
    """ unregister text/x-tinymce-output-html mimetype and transformations for captioned images """
    unregister_transform(context, "tinymce_output_html_to_html")
    unregister_transform(context, "html_to_tinymce_output_html")
    unregister_mimetype(context, 'text/x-tinymce-output-html')
    unregister_transform_policy(context, 'text/x-safe-html')
    register_transform_policy(context, "text/x-html-safe", "html_to_plone_outputfilters_html")


def importVarious(context):
    if context.readDataFile('portal-tinymce.txt') is None:
        return
    site = context.getSite()
    add_editor(site)


def unregisterUtility(context):
    my_utility = getUtility(ITinyMCE)
    context.getSiteManager().unregisterUtility(my_utility, ITinyMCE)
    del my_utility

    transaction.commit()


# BBB deprecated in Plone 4.1
deprecatedFrom("Please import from plone.outputfilters.setuphandlers instead.",
               'plone.outputfilters.setuphandlers',
               'register_mimetype',
               'unregister_mimetype',
               'register_transform',
               'unregister_transform',
               'register_transform_policy',
               'unregister_transform_policy',
               'install_mimetype_and_transforms',
               )
