from zope.interface import Interface
from zope.interface import implements
from zope.component import adapts
try:
    from plone.caching.interfaces import IRulesetLookup
    IRulesetLookup    # pyflakes
except ImportError:
    IRulesetLookup = Interface
from Products.TinyMCE.interfaces import ITinyMCECompressor
from zope.publisher.interfaces.browser import IBrowserRequest

class TinyMCEResourceLookup(object):
    """TinyMCE resource ruleset lookup.

    Returns 'plone.stableResource' for the TinyMCE
    compressor view.
    """

    implements(IRulesetLookup)
    adapts(ITinyMCECompressor, IBrowserRequest)

    def __init__(self, published, request):
        pass

    def __call__(self):
        return 'plone.stableResource'
