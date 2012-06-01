from zope.interface import implements
from zope.globalrequest import getRequest

from Products.TinyMCE.adapters.interfaces import ISchema


class ATSchema(object):
    """ Schema information of Archetype objects """
    implements(ISchema)

    prefix = ''

    def __init__(self, context):
        """Constructor"""
        self.context = context

    def getFieldNames(self, filter_field='text', filter_widget='RichWidget'):
        """ see ISchema interface """
        schema = self.context.Schema()
        return [field.getName()
                for field in schema.filterFields(type='text')
                if field.widget.getName() == 'RichWidget']

        
try:
    from plone.dexterity.schema import SCHEMA_CACHE
    from plone.app.textfield import RichText

    class DXSchema(ATSchema):
        """ Schema information of Dexterity objects """

        prefix = 'form\\\\.widgets\\\\.'

        def getportaltype(self):
            return self.context.portal_type

        def getFieldNames(self, filter_field='text', filter_widget='RichWidget'):
            """ see ISchema interface """
            schema = SCHEMA_CACHE.get(self.getportaltype())
            return [name for name, field in schema.namesAndDescriptions() if
                    isinstance(field, RichText)]


    class DXAddSchema(DXSchema):
        """ Schema information of Dexterity objects on add view
            The Plone site is the context.
        """

        def getportaltype(self):
            # put portal type in session, since there is no
            # other way to access it from the compressor
            request = getRequest()
            return request.SESSION.get('dx_add_portal_type')

except ImportError:
    pass

    # Dexteritiy is optional
