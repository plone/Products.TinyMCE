from sgmllib import SGMLParser
import re

singleton_tags = ["img", "br", "hr", "input", "meta", "param", "col"] 

class TinyMCEOutput(SGMLParser):

    from htmlentitydefs import entitydefs

    def __init__(self, context=None):
        SGMLParser.__init__(self)
        self.current_status = None
	self.context = context
	self.pieces = [] 
       
    def append_data(self, data, add_eol=0):
	if not add_eol:
	    data = data.replace("\n", "") 
	    data = data.replace("\r", "")
	data += '\n'    
	self.pieces.append(data)

    def handle_charref(self, ref):          
        self.append_data("&#%(ref)s;" % locals())

    def handle_entityref(self, ref):       
        self.append_data("&%(ref)s;" % locals())

    def handle_data(self, text):
        self.append_data(text);

    def handle_comment(self, text):          
        self.append_data("<!--%(text)s-->" % locals())

    def handle_pi(self, text):              
        self.append_data("<?%(text)s>" % locals())

    def handle_decl(self, text):
        self.append_data("<!%(text)s>" % locals())
        
    def unknown_starttag(self, tag, attrs):
        strattrs = "".join([' %s="%s"' % (key, value) for key, value in attrs])
	if tag in singleton_tags:
            self.append_data("<%(tag)s%(strattrs)s />\n" % locals())
	else:
            self.append_data("<%(tag)s%(strattrs)s>\n" % locals())
        
    def unknown_endtag(self, tag):
        self.append_data("</%(tag)s>" % locals(), add_eol=1) 

    def getResult(self):
        result = "".join(self.pieces)
        self.pieces = None
        return result
