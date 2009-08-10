from Products.CMFCore.utils import getToolByName
from Products.TinyMCE.setuphandlers import uninstall_mimetype_and_transforms, remove_editor, unregisterUtility

def uninstall(portal, reinstall=False):

    if not reinstall:

        # normal uninstall
        setup_tool = getToolByName(portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-Products.TinyMCE:uninstall')

        # http://plone.org/products/tinymce/issues/44
        uninstall_mimetype_and_transforms(portal)

        # Remove TinyMCE as a possible editor
        remove_editor(portal)

        # remove utility
        unregisterUtility(portal)

        return "Ran all uninstall steps."
