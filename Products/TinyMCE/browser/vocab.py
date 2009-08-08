from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.interface import implements

class ImageScalesVocabulary(object):
    """Vocabulary factory for wickedized portal types.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        scales = (
            ('', 'Original'),
        )
        items = []
        for scale, title in scales:
            items.append(SimpleTerm(scale, scale, title))
        return SimpleVocabulary(items)

ImageScalesVocabularyFactory = ImageScalesVocabulary()
