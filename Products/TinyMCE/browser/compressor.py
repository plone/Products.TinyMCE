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

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

def compress_string(s):
    zbuf = StringIO()
    zfile = GzipFile(mode='wb', compresslevel=6, fileobj=zbuf)
    zfile.write(s)
    zfile.close()
    return zbuf.getvalue()

def get_file_contents(context, filename):
    content = context.restrictedTraverse(filename, '') 
    return str(content)

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
        content = []
        response = self.request.response
        response.headers["Content-Type"] = "text/javascript"

        if not isJS:
            return self.tiny_mce_gzip()(base_url=JS_BASE_URL)

    #patch_vary_headers(response, ['Accept-Encoding'])

        now = datetime.utcnow()
        response['Date'] = now.strftime('%a, %d %b %Y %H:%M:%S GMT')

        # XXX caching headers like in Django?

        # Add core, with baseURL added
        content.append(get_file_contents(self.context, "tiny_mce%s.js" % suffix).replace(
                "tinymce._init();", "tinymce.baseURL='%s';tinymce._init();" % ""))

        # Patch loading functions
        content.append("tinyMCE_GZ.start();")

        # Add core languages
        for lang in languages:
            content.append(get_file_contents(self.context, "langs/%s.js" % lang))

        # Add themes
        for theme in themes:
            content.append(get_file_contents(self.context, "themes/%s/editor_template%s.js"
                    % (theme, suffix)))

            for lang in languages:
                content.append(get_file_contents(self.context, "themes/%s/langs/%s.js"
                        % (theme, lang)))

        # Add plugins
        for plugin in plugins:
            content.append(get_file_contents(self.context, "plugins/%s/editor_plugin%s.js"
                    % (plugin, suffix)))

            for lang in languages:
                content.append(get_file_contents(self.context, "plugins/%s/langs/%s.js"
                        % (plugin, lang)))

        # Restore loading functions
        content.append("tinyMCE_GZ.end();")

        # Compress
        content = ''.join(content)
        if compress:
            content = compress_string(content)
            response['Content-Encoding'] = 'gzip'
            response['Content-Length'] = str(len(content))

        
    #timeout = 3600 * 24 * 10
    #patch_response_headers(response, timeout)
#    cache.set(cacheKey, {
#        'Last-Modified': response['Last-Modified'],
#        'ETag': response['ETag'],
#    })
        return content
