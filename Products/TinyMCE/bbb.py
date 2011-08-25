# Check for Plone versions
try:
    from plone.app.upgrade import v40
    v40   # pyflakes
    HAS_PLONE40 = True
except ImportError:
    HAS_PLONE40 = False

# BBB for Z2 vs Z3 interfaces checks
def implementedOrProvidedBy(anInterface, anObject):
    if HAS_PLONE40:
        return anInterface.providedBy(anObject)
    else:
        return anInterface.isImplementedBy(anObject)
