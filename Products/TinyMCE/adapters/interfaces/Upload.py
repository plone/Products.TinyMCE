from zope.interface import Interface


class IUpload(Interface):
    """Adds the uploaded file to the folder"""

    def __init__(self, context):
        """Constructor"""

    def errorMessage(self, msg):
        """Returns an error message"""

    def okMessage(self, msg):
        """Returns an ok message"""

    def cleanupFilename(self, name):
        """Generate a unique id which doesn't matc the system generated ids"""

    def upload(self):
        """Adds uploaded file"""

    def replacefile(self):
        """ Replace the binary content of a file object """
