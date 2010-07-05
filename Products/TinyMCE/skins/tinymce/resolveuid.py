## Script (Python) "resolveuid"
##title=Retrieve an object using its UID
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
# (reference_url is supposed to do the same thing, but is broken)
from Products.CMFCore.utils import getToolByName
from Products.PythonScripts.standard import html_quote
from AccessControl import Unauthorized

request = context.REQUEST
response = request.RESPONSE

try:
    uuid = traverse_subpath.pop(0)
except:
    raise Unauthorized, context

catalog = getToolByName(context, 'portal_catalog')

brains = catalog(UID=uuid)
if len(brains) == 0:
    brain = None
else:
    brain = brains[0]

if not brain:
    hook = getattr(context, 'kupu_resolveuid_hook', None)
    if hook:
        obj = hook(uuid)
    if not obj:
        return response.notFoundError('''The link you followed appears to be broken''')
    url = obj.absolute_url()
else:
    url = brain.getURL()

if traverse_subpath:
    traverse_subpath.insert(0, url)
    target = '/'.join(traverse_subpath)
else:
    target = url

if request.QUERY_STRING:
    target += '?' + request.QUERY_STRING
return response.redirect(target, status=301)
