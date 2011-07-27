"""
Based on "TinyMCE Compressor PHP" from MoxieCode.

http://tinymce.moxiecode.com/

Copyright (c) 2008 Jason Davies
Licensed under the terms of the MIT License (see LICENSE.txt)
"""

from datetime import datetime
import os
from cStringIO import StringIO
from gzip import GzipFile

import zope.component
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.TinyMCE.interfaces.utility import ITinyMCE

def compress_string(s):
    zbuf = StringIO()
    zfile = GzipFile(mode='wb', compresslevel=6, fileobj=zbuf)
    zfile.write(s)
    zfile.close()
    return zbuf.getvalue()

def split_commas(str):
    return not str and [] or str.split(",")

class GzipCompressorView(BrowserView):

    tiny_mce_gzip = ViewPageTemplateFile('tiny_mce_gzip.js')

    def __call__(self):
        plugins = split_commas(self.request.get("plugins", ""))
        languages = split_commas(self.request.get("languages", ""))
        themes = split_commas(self.request.get("themes", ""))
        isJS = self.request.get("js", "") == "true"
        compress = self.request.get("compress", "true") == "true"
        suffix = self.request.get("suffix", "") == "_src" and "_src" or ""
        response = self.request.response
        response.headers["Content-Type"] = "text/javascript"

        plone_portal_state = zope.component.getMultiAdapter(
                (self.context, self.request), name="plone_portal_state") 
        utility = zope.component.queryUtility(ITinyMCE)
        if utility is not None and getattr(utility, 'compress', True):
            editor_js = self.__name__   # compressed version
        else:
            editor_js = "tiny_mce.js"   # non compressed version 

        base_url = '/'.join([plone_portal_state.portal_url(), editor_js])

        if not isJS:
            return self.tiny_mce_gzip(base_url=base_url)

        now = datetime.utcnow()
        response['Date'] = now.strftime('%a, %d %b %Y %H:%M:%S GMT')

        traverse = lambda name: str(self.context.restrictedTraverse(name, ''))

        # Add core, with baseURL added
        content = [traverse("tiny_mce%s.js" % suffix).replace(
                "tinymce._init();",
                "tinymce.baseURL='%s';tinymce._init();" % base_url)]

        # Add core languages
        for lang in languages:
            content.append(traverse("langs/%s.js" % lang))

        # Add themes
        for theme in themes:
            content.append(traverse("themes/%s/editor_template%s.js"
                    % (theme, suffix)))

            for lang in languages:
                content.append(traverse("themes/%s/langs/%s.js"
                        % (theme, lang)))

        # Add plugins
        for plugin in plugins:
            content.append(traverse("plugins/%s/editor_plugin%s.js"
                    % (plugin, suffix)))

            for lang in languages:
                content.append(traverse("plugins/%s/langs/%s.js"
                        % (plugin, lang)))

        # Compress
        content = ''.join(content)
        if compress:
            content = compress_string(content)
            response['Content-Encoding'] = 'gzip'
            response['Content-Length'] = str(len(content))
        return content
