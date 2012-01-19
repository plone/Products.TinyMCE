try:
    import simplejson as json
    json   # pyflakes
except ImportError:
    import json

from Acquisition import aq_inner

from zope.interface import implements
from zope.component import getUtility
from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName

from Products.TinyMCE.adapters.interfaces.JSONDetails import IJSONDetails
from Products.TinyMCE.interfaces.utility import ITinyMCE

from plone.outputfilters.browser.resolveuid import uuidFor


class JSONDetails(object):
    """Return details of the current object in JSON"""
    implements(IJSONDetails)

    def __init__(self, context):
        """Constructor"""
        self.context = context

    def getDetails(self):
        """Builds a JSON object based on the details
           of this object.
        """

        utility = getToolByName(aq_inner(self.context), 'portal_tinymce')
        anchor_portal_types = {}
        for apt in utility.containsanchors.splitlines():
            if apt and '|' in apt:
                type_, field  = apt.split('|', 1)
            else:
                type_ = apt
                field = ''
            anchor_portal_types[type_] = field

        image_portal_types = utility.imageobjects.splitlines()

        results = {}
        results['title'] = self.context.title_or_id()
        #results['url'] = self.getSiteRootRelativePath()
        results['url'] = self.context.absolute_url()
        results['description'] = self.context.Description()
        results['uid_relative_url'] = 'resolveuid/' + uuidFor(self.context)
        results['uid_url'] = self._getPloneUrl() + '/resolveuid/' + uuidFor(self.context)

        if self.context.portal_type in image_portal_types:
            images = self.context.restrictedTraverse('@@images')

            # TODO: support other contenttypes
            field_name = 'image'
            results['thumb'] = '%s/@@images/%s/%s' % (results['uid_url'], field_name, 'thumb')
            sizes = images.getAvailableSizes(field_name)
            scales = [{'value': '@@images/%s/%s' % (field_name, key),
                       'size': size,
                       'title': key.capitalize()} for key, size in sizes.items()]
            scales.sort(key=lambda x: x['size'][0])
            original_size = images.getImageSize(field_name)
            if original_size[0] < 0 or original_size[1] < 0:
                original_size = (0, 0)
            scales.insert(0, {'value': '',
                              'title': 'Original',
                              'size': original_size})
            results['scales'] = scales
        else:
            results['thumb'] = ""

        if self.context.portal_type in anchor_portal_types:
            content_anchors = self.context.restrictedTraverse('@@content_anchors')
            fieldname = anchor_portal_types[self.context.portal_type]
            results['anchors'] = content_anchors.listAnchorNames(fieldname)
        else:
            results['anchors'] = []
        results.update(self.additionalDetails())

        self.context.REQUEST.response.setHeader("Content-type", "application/json")
        return json.dumps(results)

    def additionalDetails(self):
        """Hook to allow subclasses to supplement or override the default set of results
        """
        return {}

    def _getPloneUrl(self):
        """Return the URL corresponding to the root of the Plone site."""
        portal_url = getToolByName(self.context, 'portal_url')
        portal = portal_url.getPortalObject()
        return portal.absolute_url()

    def getSiteRootRelativePath(self):
        """ Get site root relative path to an item

        @return: Path to the context object, relative to site root, prefixed with a slash.
        """

        portal_state = getMultiAdapter((self.context, self.context.REQUEST), name=u'plone_portal_state')
        site = portal_state.portal()

        # Both of these are tuples
        site_path = site.getPhysicalPath()
        context_path = self.context.getPhysicalPath()

        relative_path = context_path[len(site_path):]

        return "/" + "/".join(relative_path)
