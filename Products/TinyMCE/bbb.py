# Check for Plone versions
try:
    from plone.app.upgrade import v40
    HAS_PLONE30 = True
    HAS_PLONE40 = True
except ImportError:
    HAS_PLONE40 = False
    try:
        from Products.CMFPlone.migrations import v3_0
    except ImportError:
        HAS_PLONE30 = False
    else:
        HAS_PLONE30 = True


# BBB for Z2 vs Z3 interfaces checks
def implementedOrProvidedBy(anInterface, anObject):
    if HAS_PLONE40:
        return anInterface.providedBy(anObject)
    else:
        return anInterface.isImplementedBy(anObject)
