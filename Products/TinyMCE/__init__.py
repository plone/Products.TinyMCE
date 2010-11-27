from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.permissions import setDefaultRoles
from Products.TinyMCE.utility import TinyMCE

global tinymce_globals

tinymce_globals=globals()
PROJECTNAME = "TinyMCE"

tools = (
    TinyMCE,
    )

setDefaultRoles('Plone Site Setup: TinyMCE', ('Manager', 'Site Administrator'))

def initialize(context):
    registerDirectory('skins', tinymce_globals)

    from Products.CMFCore import utils
    utils.ToolInit("%s Tool" % PROJECTNAME,
                   tools=tools,
                   icon="browser/images/tinymce_icon.gif",
                   ).initialize(context)
