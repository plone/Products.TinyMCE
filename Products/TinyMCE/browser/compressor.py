"""
Based on "TinyMCE Compressor PHP" from MoxieCode.

http://tinymce.moxiecode.com/

Copyright (c) 2008 Jason Davies
Licensed under the terms of the MIT License (see LICENSE.txt)
"""

from datetime import datetime
import os.path

from zope.component import queryUtility, getMultiAdapter
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.ResourceRegistries.tools.packer import JavascriptPacker

from Products.TinyMCE.interfaces.utility import ITinyMCE
from Products.CMFCore.utils import getToolByName

try:
    import simplejson as json
    json  # Pyflakes
except ImportError:
    import json


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
        response.setHeader('Content-type', 'application/javascript')
        base_url = '/'.join([self.context.absolute_url(), self.__name__])
        # fix for Plone <4.1 http://dev.plone.org/plone/changeset/48436
        # only portal_factory part of condition!
        if 'portal_factory' or '++contextportlets++' in base_url:
            portal_state = getMultiAdapter((self.context, self.request),
			    name="plone_portal_state")
            base_url = '/'.join([portal_state.portal_url(), self.__name__])

        config = getToolByName(self.context,'portal_tinymce').getConfiguration(
                context=self.context,
                request=self.request,
                script_url=base_url,
            )

        if not isJS:
            tiny_mce_gzip = self.tiny_mce_gzip(tinymce_json_config=config)
	    # XXX don't do this in debug mode
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

        # add custom plugins
        config = json.loads(config)
        customplugins = {}
        for plugin in config['customplugins']:
            if '|' in plugin:
                name, path = plugin.split('|', 1)
                customplugins[name] = path

                content.append('tinymce.PluginManager.load("%s", "%s/%s");' % (
                    name, config['portal_url'], path));

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
            if plugin in customplugins:
                script = customplugins[plugin]
                path, bn = os.path.split(customplugins[plugin])
            else:
                script = "plugins/%s/editor_plugin%s.js" % (plugin, suffix)
                path = 'plugins/%s' % plugin

            content.append(traverse(script))

            for lang in languages:
                content.append(traverse("%s/langs/%s.js" % (path, lang)))

        # TODO: add aditional javascripts in plugins

        return ''.join(content)
