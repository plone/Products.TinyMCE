"""
Based on "TinyMCE Compressor PHP" from MoxieCode.

http://tinymce.moxiecode.com/

Copyright (c) 2008 Jason Davies
Licensed under the terms of the MIT License (see LICENSE.txt)
"""
import os.path

from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from zope.component import getMultiAdapter

from Products.TinyMCE.interfaces import ITinyMCECompressor


def isContextUrl(url):
    """Some url do not represent context. Check is based on url. If
    fragment are detected, this method return False
    fragments are portal_factory, ++contextportlets++, ++groupportlets++,
    ++contenttypeportlets++
    """
    fragments = ('portal_factory', '++contextportlets++', '++groupportlets++',
                '++contenttypeportlets++')

    for fragment in fragments:
        if fragment in url:
            return False

    return True


def string_template(filename):
    path = os.path.dirname(__file__)
    f = open(os.path.join(path, filename), 'rb')
    try:
        body = f.read()
    finally:
        f.close()

    body = body.decode('utf-8')
    template = lambda **kwargs: body % kwargs
    return staticmethod(template)


class TinyMCECompressorView(BrowserView):
    """ Bundle TinyMCE editor and all resources """

    implements(ITinyMCECompressor)

    tiny_mce_gzip = string_template('tiny_mce_gzip.js')

    def __call__(self):
        """Parameters are parsed from url query as defined by tinymce"""
        plugins = self.request.get("plugins", "").split(',')
        languages = self.request.get("languages", "").split(',')
        isJS = self.request.get("js", "") == "true"
        themes = self.request.get("themes", "").split(',')
        suffix = self.request.get("suffix", "") == "_src" and "_src" or ""

        # set correct content type
        response = self.request.response
        response.setHeader('Content-type', 'application/javascript')

        if not isJS:
            return self.tiny_mce_gzip()

        # get base_url
        base_url = '/'.join([self.context.absolute_url(), self.__name__])
        # fix for Plone <4.1 http://dev.plone.org/plone/changeset/48436
        # only portal_factory part of condition!
        if not isContextUrl(base_url):
            portal_state = getMultiAdapter((self.context, self.request),
                name="plone_portal_state")
            base_url = '/'.join([portal_state.portal_url(), self.__name__])

        # use traverse so developers can override tinymce through skins
        traverse = lambda name: str(self.context.restrictedTraverse(name, ''))

        # add core javascript file with configure ajax call
        content = [
            traverse("tiny_mce%s.js" % suffix).replace(
                "tinymce._init();",
                "tinymce.baseURL='%s';tinymce._init();" % base_url)
        ]

        portal_tinymce = getToolByName(self.context, 'portal_tinymce')
        customplugins = {}
        for plugin in portal_tinymce.customplugins.splitlines():
            if '|' in plugin:
                name, path = plugin.split('|', 1)
                customplugins[name] = path
                content.append('tinymce.PluginManager.load("%s", "%s/%s");' % (
                    name, getToolByName(self.context, 'portal_url')(), path))
            else:
                plugins.append(plugin)

        # Add plugins
        for plugin in set(plugins):
            if plugin in customplugins:
                script = customplugins[plugin]
                path, bn = customplugins[plugin].lstrip('/').split('/', 1)
            else:
                script = "plugins/%s/editor_plugin%s.js" % (plugin, suffix)
                path = 'plugins/%s' % plugin

            content.append(traverse(script))

            for lang in languages:
                content.append(traverse("%s/langs/%s.js" % (path, lang)))

        # Add core languages
        for lang in languages:
            content.append(traverse("langs/%s.js" % lang))

        # Add themes
        for theme in themes:
            content.append(traverse("themes/%s/editor_template%s.js" % (theme, suffix)))

            for lang in languages:
                content.append(traverse("themes/%s/langs/%s.js" % (theme, lang)))

        # TODO: add additional javascripts in plugins

        return ''.join(content)
