"""
Based on "TinyMCE Compressor PHP" from MoxieCode.

http://tinymce.moxiecode.com/

Copyright (c) 2008 Jason Davies
Licensed under the terms of the MIT License (see LICENSE.txt)
"""

from datetime import datetime

from zope.component import queryUtility
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.ResourceRegistries.tools.packer import JavascriptPacker

from Products.TinyMCE.interfaces.utility import ITinyMCE


class TinyMCECompressorView(BrowserView):
    tiny_mce_gzip = ViewPageTemplateFile('tiny_mce_gzip.js')

    # TODO: cache
    def __call__(self):
        plugins = self.request.get("plugins", "").split(',')
        languages = self.request.get("languages", "").split(',')
        themes = self.request.get("themes", "").split(',')
        isJS = self.request.get("js", "") == "true"
        suffix = self.request.get("suffix", "") == "_src" and "_src" or ""
        response = self.request.response
        response.headers["Content-Type"] = "text/javascript"
        base_url = '/'.join([self.context.absolute_url(), self.__name__])

        if not isJS:
            config = queryUtility(ITinyMCE).getConfiguration(
                context=self.context,
                request=self.request,
                script_url=base_url,
            )

            tiny_mce_gzip = self.tiny_mce_gzip(tinymce_json_config=config)
            return JavascriptPacker('full').pack(tiny_mce_gzip)

        now = datetime.utcnow()
        response['Date'] = now.strftime('%a, %d %b %Y %H:%M:%S GMT')

        traverse = lambda name: str(self.context.restrictedTraverse(name, ''))

        # Add core, with baseURL added
        content = [
            traverse("tiny_mce%s.js" % suffix).replace(
                "tinymce._init();",
                "tinymce.baseURL='%s';tinymce._init();" % base_url)
        ]

        # Add core languages
        # TODO: we have our own translations
        for lang in languages:
            content.append(traverse("langs/%s.js" % lang))

        # Add themes
        for theme in themes:
            content.append(traverse("themes/%s/editor_template%s.js" % (theme, suffix)))

            for lang in languages:
                content.append(traverse("themes/%s/langs/%s.js" % (theme, lang)))

        # Add plugins
        for plugin in plugins:
            content.append(traverse("plugins/%s/editor_plugin%s.js" % (plugin, suffix)))

            for lang in languages:
                content.append(traverse("plugins/%s/langs/%s.js" % (plugin, lang)))

        # TODO: add aditional javascripts in plugins

        return ''.join(content)
