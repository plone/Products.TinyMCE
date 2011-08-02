from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IContextSourceBinder
from zope.component import getUtilitiesFor
from zope.interface import provider


@provider(IContextSourceBinder)
def shortcuts_vocabulary(context):
    from Products.TinyMCE.interfaces.shortcut import ITinyMCEShortcut  # circular dependency
    terms = []
    for name, utility in getUtilitiesFor(ITinyMCEShortcut):
        terms.append(SimpleVocabulary.createTerm(utility.title, str(name), name))
    return SimpleVocabulary(terms)
