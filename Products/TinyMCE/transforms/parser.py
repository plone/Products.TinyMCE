from Products.CMFCore.utils import getToolByName

from sgmllib import SGMLParser, SGMLParseError
from urlparse import urlsplit, urljoin, unquote

HAS_LINGUAPLONE = True
try:
    from Products.LinguaPlone.utils import translated_references
except ImportError:
    HAS_LINGUAPLONE = False

singleton_tags = ["img", "br", "hr", "input", "meta", "param", "col"]

class TinyMCEOutput(SGMLParser):
    """ Parser to convert UUID links and captioned images """
    from htmlentitydefs import entitydefs

    def __init__(self, context=None, captioned_images=0):
        SGMLParser.__init__(self)
        self.current_status = None
        self.context = context
        self.captioned_images = captioned_images
        self.pieces = []

    def append_data(self, data, add_eol=0):
        """Append data unmodified to self.data, add_eol adds a newline character"""
        if add_eol:
            data += '\n'
        self.pieces.append(data)

    def handle_charref(self, ref):
        """ Handle characters, just add them again """
        self.append_data("&#%(ref)s;" % locals())

    def handle_entityref(self, ref):
        """ Handle html entities, put them back as we get them """
        self.append_data("&%(ref)s;" % locals())

    def handle_data(self, text):
        """ Add data unmodified """
        self.append_data(text)

    def handle_comment(self, text):
        """ Handle comments unmodified """
        self.append_data("<!--%(text)s-->" % locals())

    def handle_pi(self, text):
        """ Handle processing instructions unmodified"""
        self.append_data("<?%(text)s>" % locals())

    def handle_decl(self, text):
        """Handle declarations unmodified """
        self.append_data("<!%(text)s>" % locals())

    def lookup_uid(self, uid):
        context = self.context
        if HAS_LINGUAPLONE:
            # If we have LinguaPlone installed, add support for language-aware
            # references
            uids = translated_references(context, context.Language(), uid)
            if len(uids) > 0:
                uid = uids[0]
        reference_tool = getToolByName(context, 'reference_catalog')
        return reference_tool.lookupObject(uid)

    def unknown_starttag(self, tag, attrs):
        """Here we've got the actual conversion of links and images. Convert UUID's to absolute url's, and process captioned images to HTML"""
        if tag in ['a', 'img']:
            # Only do something if tag is a link or images
            attributes = {}
            for (key, value) in attrs:
                attributes[key] = value

            if tag == 'a':
                if attributes.has_key('href'):
                    href = attributes['href']
                    if 'resolveuid' in href:
                        # We should check if "Link using UIDs" is enabled in
                        # the TinyMCE tool, but then the kupu resolveuid is
                        # used, so let's always transform here
                        parts = href.split("/")
                        # Get the actual UUID
                        uid = parts[1]
                        appendix = ""
                        if len(parts) > 2:
                            # There is more than just the UUID, save it in
                            # appendix
                            appendix = "/".join(parts[2:])

                        # move name of links to anchors to appendix
                        # (resolveuid/12fc34#anchor)
                        if '#' in uid:
                            uid, anchor = uid.split('#')
                            appendix = '#%s' % anchor  #anchor + appendix won't happen

                        ref_obj = self.lookup_uid(uid)
                        if ref_obj:
                            href = ref_obj.absolute_url() + appendix
                            attributes['href'] = href
                            attrs = attributes.iteritems()
            elif tag == 'img':
                # First collect some attributes
                src = ""
                description = ""
                if attributes.has_key("src"):
                    src = attributes["src"]
                if 'resolveuid' in src:
                    # We need to convert the UUID to a relative path here
                    parts = src.split("/")
                    uid = parts[1]
                    appendix = ""
                    if len(parts) > 2:
                        # There is more than just the UUID, save it in appendix (query parameters for example)
                        appendix = "/" + "/".join(parts[2:])
                    image_obj = self.lookup_uid(uid)
                    if image_obj:
                        # Only do something when the image is actually found in the reference_catalog
                        src = image_obj.absolute_url() + appendix
                        attributes["src"] = src
                        if hasattr(image_obj, "Description"):
                            description = image_obj.Description()
                else:
                    # It's a relative path, let's see if we can get the description from the portal catalog
                    full_path = urljoin(self.context.absolute_url(), src)
                    #remove any encoded characters
                    full_path = unquote(full_path)
                    scheme, netloc, path, query, fragment = urlsplit(full_path)
                    portal_catalog = getToolByName(self.context, "portal_catalog")
                    # Check if we can find this in the portal catalog
                    brains = portal_catalog({'path' : {'query':path}, 'type' : 'Image'})
                    if len(brains) == 0:
                        # Maybe something like 'image_preview' is in the path, let's chop it
                        query= {'path' : {'query' : "/".join(path.split('/')[:-1])}, 'type' : 'Image'}
                        brains = portal_catalog(query)
                    if len(brains) > 0:
                        description = brains[0].Description
                # Check if the image is a captioned image
                classes = ""
                if attributes.has_key("class"):
                    classes = attributes["class"]
                # if we set an description within tinymce we want to keep that one
                if attributes.has_key("alt") and attributes["alt"]:
                    description = attributes["alt"]
                if self.captioned_images and classes.find('captioned') != -1:
                    # We have captioned images, and we need to convert them, so let's do so
                    width_style = ""
                    if attributes.has_key("width"):
                        width_style="style=\"width:%spx;\" " % attributes["width"]
                    image_attributes = ""
                    image_attributes = image_attributes.join(["%s %s=\"%s\"" % (image_attributes, key, value) for (key, value) in attributes.items() if not key in ["class", "src"]])
                    captioned_html = """<dl %sclass="%s">
                                        <dt %s>
                                            <img %s src="%s"/>
                                        </dt>
                                        <dd class="image-caption">%s</dd>
                                        </dl>""" % (width_style, classes, width_style, image_attributes, src ,description)
                    self.append_data(captioned_html)
                    return True
                else:
                    # Nothing happens with the image, so add it normally
                    attrs = attributes.iteritems()

        # Add the tag to the result
        strattrs = "".join([' %s="%s"' % (key, value) for key, value in attrs])
        if tag in singleton_tags:
            self.append_data("<%(tag)s%(strattrs)s />" % locals())
        else:
            self.append_data("<%(tag)s%(strattrs)s>" % locals())

    def unknown_endtag(self, tag):
        """Add the endtag unmodified"""
        self.append_data("</%(tag)s>" % locals())

    def parse_declaration(self, i):
        """Fix handling of CDATA sections. Code borrowed from BeautifulSoup.
        """
        j = None
        if self.rawdata[i:i+9] == '<![CDATA[':
             k = self.rawdata.find(']]>', i)
             if k == -1:
                 k = len(self.rawdata)
             data = self.rawdata[i+9:k]
             j = k+3
             self.append_data("<![CDATA[%s]]>" % data)
        else:
            try:
                j = SGMLParser.parse_declaration(self, i)
            except SGMLParseError:
                toHandle = self.rawdata[i:]
                self.handle_data(toHandle)
                j = i + len(toHandle)
        return j

    def getResult(self):
        """Return the parsed result and flush it"""
        result = "".join(self.pieces)
        self.pieces = None
        return result
