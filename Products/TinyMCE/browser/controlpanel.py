from zope.interface import implements
from zope.i18nmessageid import MessageFactory
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.event import notify

from plone.fieldsets.fieldsets import FormFieldsets
from plone.app.controlpanel.form import ControlPanelForm
from plone.app.controlpanel.events import ConfigurationChangedEvent
from plone.app.form.validators import null_validator
from plone.protect import CheckAuthenticator

from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

from Products.TinyMCE.interfaces.utility import ITinyMCELayout
from Products.TinyMCE.interfaces.utility import ITinyMCEToolbar
from Products.TinyMCE.interfaces.utility import ITinyMCELibraries
from Products.TinyMCE.interfaces.utility import ITinyMCEResourceTypes

from Products.TinyMCE.browser.interfaces.controlpanel import ITinyMCEControlPanelForm
from Products.TinyMCE import TMCEMessageFactory as _
from Products.CMFPlone import PloneMessageFactory as __


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

    form_fields = FormFieldsets(
                        tinymcelayout,
                        tinymcetoolbar,
                        tinymceresourcetypes,
                        tinymcelibraries
                        )

    label = _(u"TinyMCE Settings")
    description = _(u"Settings for the TinyMCE Wysiwyg editor.")
    form_name = _("TinyMCE Settings")

    @form.action(__(u'label_save', default=u'Save'), name=u'save')
    def handle_edit_action(self, action, data):
        CheckAuthenticator(self.request)
        if form.applyChanges(self.context, self.form_fields, data,
                             self.adapters):
            self.status = __("Changes saved.")
            notify(ConfigurationChangedEvent(self, data))
            self._on_save(data)
        else:
            self.status = __("No changes made.")

    @form.action(__(u'label_cancel', default=u'Cancel'),
                validator=null_validator,
                name=u'cancel')
    def handle_cancel_action(self, action, data):
        IStatusMessage(self.request).addStatusMessage(__("Changes canceled."),
                                                        type="info")
        portal = getToolByName(self.context, name='portal_url')\
            .getPortalObject()
        url = getMultiAdapter((portal, self.request),
                                name='absolute_url')()
        self.request.response.redirect(url + '/plone_control_panel')
        return ''
