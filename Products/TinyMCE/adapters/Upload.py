from Acquisition import aq_inner
from Acquisition import aq_parent
from zExceptions import BadRequest
from zope.app.content import queryContentType
from zope.i18n import translate
from zope.schema import getFieldsInOrder
from Products.CMFCore.interfaces._content import IFolderish
from Products.CMFCore.utils import getToolByName
from plone.outputfilters.browser.resolveuid import uuidFor
from zope.interface import implements
from zope.i18nmessageid import MessageFactory

from Products.TinyMCE.adapters.interfaces.Upload import IUpload

import pkg_resources
try:
    pkg_resources.get_distribution('plone.dexterity')
except pkg_resources.DistributionNotFound:
    HAS_DEXTERITY = False
    pass
else:
    HAS_DEXTERITY = True
    from plone.dexterity.interfaces import IDexterityContent
    from plone.namedfile.interfaces import INamedField
    from plone.rfc822.interfaces import IPrimaryFieldInfo


TEMPLATE = """
<html>
<head></head>
<body onload="%s"></body>
</html>
"""

_ = MessageFactory('plone.tinymce')


class Upload(object):
    """Adds the uploaded file to the folder"""
    implements(IUpload)

    def __init__(self, context):
        """Constructor"""
        self.context = context

    def errorMessage(self, msg):
        """Returns an error message"""
        msg = translate(msg, context=self.context.REQUEST)
        script = TEMPLATE % (
            "window.parent.uploadError('" + msg.replace("'", "\\'") + "');")
        return script

    def okMessage(self, path, folder):
        """Returns an ok message"""
        script = TEMPLATE % (
            "window.parent.uploadOk('" + \
            path.replace("'", "\\'") + "', '" + \
            folder.replace("'", "\\'") + "');")
        return script

    def cleanupFilename(self, name):
        """Generate a unique id which doesn't match	the system generated ids"""

        context = self.context
        id = ''
        name = name.replace('\\', '/')  # Fixup Windows filenames
        name = name.split('/')[-1]  # Throw away any path part.
        for c in name:
            if c.isalnum() or c in '._':
                id += c

        # Raise condition here, but not a lot we can do about that
        if context.check_id(id) is None and getattr(context, id, None) is None:
            return id

        # Now make the id unique
        count = 1
        while 1:
            if count == 1:
                sc = ''
            else:
                sc = str(count)
            newid = "copy%s_of_%s" % (sc, id)
            if context.check_id(newid) is None and \
               getattr(context, newid, None) is None:
                return newid
            count += 1

    def upload(self):
        """Adds uploaded file.

        Required params: uploadfile, uploadtitle, uploaddescription
        """
        context = aq_inner(self.context)
        if not IFolderish.providedBy(context):
            context = aq_parent(context)

        request = context.REQUEST
        ctr_tool = getToolByName(context, 'content_type_registry')
        utility = getToolByName(context, 'portal_tinymce')

        uploadfile = request['uploadfile']
        id = uploadfile.filename
        content_type = uploadfile.headers["Content-Type"]
        typename = ctr_tool.findTypeName(id, content_type, "")

        # Permission checks based on code by Danny Bloemendaal

        # 1) check if the current user has permissions to add stuff
        if not context.portal_membership.checkPermission(
            'Add portal content', context):
            return self.errorMessage(
                _("You do not have permission to upload files in this folder"))

        # 2) check image types uploadable in folder.
        #    priority is to content_type_registry image type
        allowed_types = [t.id for t in context.getAllowedTypes()]
        if typename in allowed_types:
            uploadable_types = [typename]
        else:
            uploadable_types = []

        if content_type.split('/')[0] == 'image':
            image_portal_types = utility.imageobjects.split('\n')
            uploadable_types += [t for t in image_portal_types
                                    if t in allowed_types
                                       and t not in uploadable_types]

        # Get an unused filename without path
        id = self.cleanupFilename(id)

        for metatype in uploadable_types:
            try:
                newid = context.invokeFactory(type_name=metatype, id=id)
                if newid is None or newid == '':
                    newid = id
                break
            except ValueError:
                continue
            except BadRequest:
                return self.errorMessage(_("Bad filename, please rename."))
        else:
            return self.errorMessage(
                _("Not allowed to upload a file of this type to this folder"))

        obj = getattr(context, newid, None)

        # Set title + description.
        # Attempt to use Archetypes mutator if there is one, in case it uses
        # a custom storage
        title = request['uploadtitle']
        description = request['uploaddescription']

        if title:
            try:
                obj.setTitle(title)
            except AttributeError:
                obj.title = title

        if description:
            try:
                obj.setDescription(description)
            except AttributeError:
                obj.description = description

        if HAS_DEXTERITY and IDexterityContent.providedBy(obj):
            if not self.setDexterityItem(obj, uploadfile):
                return self.errorMessage(
                        _("The content-type '${type}' has no blob-field!",
                          mapping={'type': metatype}))
        else:
            # set primary field
            pf = obj.getPrimaryField()
            pf.set(obj, uploadfile)

        if not obj:
            return self.errorMessage(_("Could not upload the file"))

        obj.reindexObject()
        folder = obj.aq_parent.absolute_url()

        if utility.link_using_uids:
            path = "resolveuid/%s" % (uuidFor(obj))
        else:
            path = obj.absolute_url()
        return self.okMessage(path, folder)

    def setDexterityItem(self, obj, uploadfile):
        """ Set the blob-field of dexterity-based types

        This works with blob-types of plone.app.contenttypes and has
        fallbacks for other implementations of blob-types with dexterity.

        """
        field_name = ''
        info = ''
        try:
            # Use the primary field if it's an blob-field
            info = IPrimaryFieldInfo(obj, None)
        except TypeError:
            # ttw-types without a primary field throw a TypeError on
            # IPrimaryFieldInfo(obj, None)
            pass
        if info:
            field = info.field
            if INamedField.providedBy(field):
                field_name = info.fieldname
        if not field_name:
            # Use the first blob-field in the schema
            obj_schema = queryContentType(obj)
            obj_fields = getFieldsInOrder(obj_schema)
            for field_info in obj_fields:
                field = field_info[1]
                if INamedField.providedBy(field):
                    field_name = field_info[0]
                    break
        if not field_name:
            return False
        else:
            # Create either a NamedBlobImage or a NamedImage
            setattr(obj, field_name, field._type(uploadfile.read(),
                                                 filename=unicode(id)))
        return True

    def setDescription(self, description):
        aq_inner(self.context).setDescription(description)
