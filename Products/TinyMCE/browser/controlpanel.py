from zope.interface import implements
from zope.formlib import form
from zope.i18nmessageid import MessageFactory
from plone.fieldsets.fieldsets import FormFieldsets

from plone.app.controlpanel.form import ControlPanelForm

from Products.Five.formlib import formbase
from Acquisition import aq_inner
from Products.Five.browser import BrowserView

from Products.CMFCore.utils import getToolByName
from Products.PythonScripts.standard import html_quote, newline_to_br

from Products.TinyMCE.interfaces.utility import ITinyMCE
from Products.TinyMCE.interfaces.utility import ITinyMCELayout
from Products.TinyMCE.interfaces.utility import ITinyMCEToolbar
from Products.TinyMCE.interfaces.utility import ITinyMCELibraries
from Products.TinyMCE.interfaces.utility import ITinyMCEResourceTypes

from Products.TinyMCE.browser.interfaces.controlpanel import ITinyMCEControlPanelForm
from Products.TinyMCE.setuphandlers import install_mimetype_and_transforms, uninstall_mimetype_and_transforms

_ = MessageFactory('tinymce')

class TinyMCEControlPanelForm(ControlPanelForm):
    """TinyMCE Control Panel Form"""
    implements(ITinyMCEControlPanelForm)

    tinymcelayout = FormFieldsets(ITinyMCELayout)
    tinymcelayout.id = 'tinymcelayout'
    tinymcelayout.label = _(u'tinymcelayout', default=u'Layout')

    tinymcetoolbar = FormFieldsets(ITinyMCEToolbar)
    tinymcetoolbar.id = 'tinymcetoolbar'
    tinymcetoolbar.label = _(u'tinymcetoolbar', default=u'Toolbar')

    tinymcelibraries = FormFieldsets(ITinyMCELibraries)
    tinymcelibraries.id = 'tinymcelibraries'
    tinymcelibraries.label = _(u'tinymcelibraries', default=u'Libraries')

    tinymceresourcetypes = FormFieldsets(ITinyMCEResourceTypes)
    tinymceresourcetypes.id = 'tinymceresourcetypes'
    tinymceresourcetypes.label = _(u'tinymceresourcetypes', default=u'Resource Types')

    form_fields = FormFieldsets(tinymcelayout, tinymcetoolbar, tinymceresourcetypes) # tinymcelibraries

    label = _(u"TinyMCE Settings")
    description = _(u"Settings for the TinyMCE Wysiwyg editor.")
    form_name = _("TinyMCE Settings")

    def _on_save(self, data=None):
        """On save event handler"""
        if self.context.link_using_uids or self.context.allow_captioned_images:
            # We need to register our mimetype and transforms for uid links and captioned_images
            install_mimetype_and_transforms(self.context)
        else:
            # Unregister them
            uninstall_mimetype_and_transforms(self.context)        
