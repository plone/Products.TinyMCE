from zope.interface import Interface, Attribute


class ITinyMCEShortcut(Interface):
    """This interface defines browser shortcut"""

    title = Attribute("""Translatable name of shortcuts, appears in content browser""")

    def render(self, context):
        """Renders a list of shortcuts HTML."""
