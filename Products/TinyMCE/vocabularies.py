from plone.app.imaging.utils import getAllowedSizes
from zope.component import getUtilitiesFor
from zope.interface import provider
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IContextSourceBinder


@provider(IContextSourceBinder)
def shortcuts_vocabulary(context):
    from Products.TinyMCE.interfaces.shortcut import ITinyMCEShortcut  # circular dependency
    terms = []
    for name, utility in getUtilitiesFor(ITinyMCEShortcut):
        terms.append(SimpleVocabulary.createTerm(name, str(name), utility.title))
    return SimpleVocabulary(terms)


@provider(IContextSourceBinder)
def thumbnail_sizes_vocabulary(context):
    terms = []
    # TODO: we should query utility, but it's not certain it will be there
    for name, size in getAllowedSizes().iteritems():
        terms.append(SimpleVocabulary.createTerm(tuple((name,) + size), str(name), u"%s %s" % (name, size)))
    return SimpleVocabulary(terms)
