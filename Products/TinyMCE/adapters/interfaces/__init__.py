import zope.interface

class ISchema(zope.interface.Interface):
    """ A schema abstraction for AT and DX content """

    prefix = zope.interface.Attribute("Form prefix in add/edit-view")

    def getFieldNames(filter=None):
        """ Get names of schema fields filtered by type """
