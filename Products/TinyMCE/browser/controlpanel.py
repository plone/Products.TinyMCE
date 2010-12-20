from zope.interface import implements
from zope.i18nmessageid import MessageFactory
from plone.fieldsets.fieldsets import FormFieldsets
from plone.app.controlpanel.form import ControlPanelForm

from Products.TinyMCE.interfaces.utility import ITinyMCELayout
from Products.TinyMCE.interfaces.utility import ITinyMCEToolbar
from Products.TinyMCE.interfaces.utility import ITinyMCELibraries
from Products.TinyMCE.interfaces.utility import ITinyMCEResourceTypes

from Products.TinyMCE.browser.interfaces.controlpanel import ITinyMCEControlPanelForm

_ = MessageFactory('plone.tinymce')


class TinyMCEControlPanelForm(ControlPanelForm):
    """TinyMCE Control Panel Form"""
    implements(ITinyMCEControlPanelForm)

    tinymcelayout = FormFieldsets(ITinyMCELayout)
    tinymcelayout.id = 'tinymcelayout'
    tinymcelayout.label = _(u'Layout')

    tinymcetoolbar = FormFieldsets(ITinyMCEToolbar)
    tinymcetoolbar.id = 'tinymcetoolbar'
    tinymcetoolbar.label = _(u'Toolbar')

    tinymcelibraries = FormFieldsets(ITinyMCELibraries)
    tinymcelibraries.id = 'tinymcelibraries'
    tinymcelibraries.label = _(u'Libraries')

    tinymceresourcetypes = FormFieldsets(ITinyMCEResourceTypes)
    tinymceresourcetypes.id = 'tinymceresourcetypes'
    tinymceresourcetypes.label = _(u'Resource Types')

    form_fields = FormFieldsets(tinymcelayout, tinymcetoolbar, tinymceresourcetypes) # tinymcelibraries

    label = _(u"TinyMCE Settings")
    description = _(u"Settings for the TinyMCE Wysiwyg editor.")
    form_name = _("TinyMCE Settings")
