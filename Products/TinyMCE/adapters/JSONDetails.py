try:
    import json
except ImportError:
    import simplejson as json

from zope.interface import implements
from zope.component import getUtility

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

        utility = getUtility(ITinyMCE)
        anchor_portal_types = utility.containsanchors.split('\n')
        image_portal_types = utility.imageobjects.split('\n')

        results = {}
        results['title'] = self.context.title_or_id()
        results['url'] = self.context.absolute_url()
        results['description'] = self.context.Description()

        if self.context.portal_type in image_portal_types:
            results['uid_url'] = self._getPloneUrl() + '/resolveuid/' + uuidFor(self.context)
            # TODO: ??
            field_name = 'image'
            images = self.context.restrictedTraverse('@@images')

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
            results['anchors'] = content_anchors.listAnchorNames()
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
