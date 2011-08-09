from Acquisition import aq_inner
from AccessControl.unauthorized import Unauthorized
from zope.interface import implements
from zope.component import getUtility

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces._content import IFolderish
from plone.outputfilters.browser.resolveuid import uuidFor

from Products.TinyMCE.interfaces.utility import ITinyMCE
from Products.TinyMCE.adapters.interfaces.Upload import IUpload
from Products.TinyMCE import TMCEMessageFactory as _
from zope.i18n import translate

TEMPLATE = """
<html>
<head></head>
<body onload="%s"></body>
</html>
"""


class Upload(object):
    """Adds the uploaded file to the folder"""
    implements(IUpload)

    def __init__(self, context):
        """Constructor"""

        self.context = context

    def errorMessage(self, msg):
        """Returns an error message"""
        msg = translate(msg, context=self.context.REQUEST)
        script = TEMPLATE % ("window.parent.uploadError('" + msg.replace("'", "\\'") + "');")
        return script

    def okMessage(self, msg):
        """Returns an ok message"""
        script = TEMPLATE % ("window.parent.uploadOk('" + msg.replace("'", "\\'") + "');")
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
            if context.check_id(newid) is None and getattr(context, newid, None) is None:
                return newid
            count += 1

    def upload(self):
        """Adds uploaded file"""

        object = aq_inner(self.context)
        if not IFolderish.providedBy(object):
            object = object.getParentNode()

        context = self.context
        request = context.REQUEST
        ctr_tool = getToolByName(self.context, 'content_type_registry')
        utility = getUtility(ITinyMCE)

        id = request['uploadfile'].filename
        content_type = request['uploadfile'].headers["Content-Type"]
        typename = ctr_tool.findTypeName(id, content_type, "")

        # Permission checks based on code by Danny Bloemendaal

        # 1) check if the current user has permissions to add stuff
        if not context.portal_membership.checkPermission('Add portal content', context):
            return self.errorMessage(_("You do not have permission to upload files in this folder"))

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

        title = request['uploadtitle']
        description = request['uploaddescription']

        for metatype in uploadable_types:
            try:
                newid = context.invokeFactory(type_name=metatype, id=id)
                if newid is None or newid == '':
                    newid = id

                obj = getattr(context, newid, None)

                # set primary field
                pf = obj.getPrimaryField()
                pf.set(obj, request['uploadfile'])
                break

            except ValueError:
                continue
        else:
            return self.errorMessage(_("Not allowed to upload a file of this type to this folder"))


        # Set title + description.
        # Attempt to use Archetypes mutator if there is one, in case it uses a custom storage
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

        if not obj:
            return self.errorMessage(_("Could not upload the file"))

        obj.reindexObject()

        if utility.link_using_uids:
            return self.okMessage("resolveuid/%s" % (uuidFor(obj)))

        return self.okMessage("%s" % (obj.absolute_url()))

    def setDescription(self, description):
        self.context.setDescription(description)
