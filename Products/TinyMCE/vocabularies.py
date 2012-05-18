from plone.app.imaging.utils import getAllowedSizes
from zope.component import getUtilitiesFor
from zope.interface import directlyProvides
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IContextSourceBinder


def shortcuts_vocabulary(context):
    from Products.TinyMCE.interfaces.shortcut import ITinyMCEShortcut  # circular dependency
    terms = []
    for name, utility in getUtilitiesFor(ITinyMCEShortcut):
        terms.append(SimpleVocabulary.createTerm(name, str(name), utility.title))
    return SimpleVocabulary(terms)


directlyProvides(shortcuts_vocabulary, IContextSourceBinder)


def thumbnail_sizes_vocabulary(context):
    """Builds a vocabulary of thumbnail sizes. An example item in vocabulary
    would have title set to "tile (64, 64)" and value to ('tile', 64, 64).

    :returns: Vocabulary items for each allowed thumbnail size."
    rtype: SimpleVocabulary
    """
    terms = []
    # TODO: we should query utility, but it's not certain it will be there
    for name, size in getAllowedSizes().iteritems():
        terms.append(SimpleVocabulary.createTerm(tuple((name,) + size), str(name), u"%s %s" % (name, size)))
    return SimpleVocabulary(terms)


directlyProvides(thumbnail_sizes_vocabulary, IContextSourceBinder)


def plugins_vocabulary(context):
    """ A vocabulary containing all the allowed plugins for TinyMCE
    """
    from Products.TinyMCE.interfaces.utility import DEFAULT_PLUGINS
    plugins = DEFAULT_PLUGINS[:]
    plugins.sort()
    return SimpleVocabulary.fromValues(plugins)


directlyProvides(plugins_vocabulary, IContextSourceBinder)
