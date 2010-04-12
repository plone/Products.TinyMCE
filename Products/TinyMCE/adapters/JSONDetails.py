from zope.interface import implements
from zope.component import getUtility

try:
    import json
except:
    import simplejson as json

# Not available in xml.etree
from elementtree import HTMLTreeBuilder

from Products.TinyMCE.adapters.interfaces.JSONDetails import IJSONDetails
from Products.TinyMCE.interfaces.utility import ITinyMCE


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
        results['description'] = self.context.Description()

        if self.context.portal_type in image_portal_types:
            results['thumb'] = self.context.absolute_url() + "/image_thumb"
            results['scales'] = utility.getImageScales(self.context.getPrimaryField(),
                                                       context=self.context)
        else:
            results['thumb'] = ""

        if self.context.portal_type in anchor_portal_types:
            results['anchors'] = []
            tree = HTMLTreeBuilder.TreeBuilder()
            tree.feed('<root>%s</root>' % self.context.getPrimaryField().getAccessor(self.context)())
            rootnode = tree.close()
            for x in rootnode.getiterator():
                if x.tag == "a":
                    if "name" in x.keys():
                        results['anchors'].append(x.attrib['name'])
        else:
            results['anchors'] = []

        return json.dumps(results)
