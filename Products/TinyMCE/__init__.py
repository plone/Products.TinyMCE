from Products.CMFCore.DirectoryView import registerDirectory
from Products.TinyMCE.utility import TinyMCE

global tinymce_globals

tinymce_globals=globals()
PROJECTNAME = "TinyMCE"

tools = (
    TinyMCE,
    )

def initialize(context):
    registerDirectory('skins', tinymce_globals)

    from Products.CMFCore import utils
    utils.ToolInit("%s Tool" % PROJECTNAME,
                   tools=tools,
                   icon="browser/images/tinymce_icon.gif",
                   ).initialize(context)
