"""
Based on "TinyMCE Compressor PHP" from MoxieCode.

http://tinymce.moxiecode.com/

Copyright (c) 2008 Jason Davies
Licensed under the terms of the MIT License (see LICENSE.txt)
"""

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


TINY_MCE_GZIP = """
jQuery(function($){

  function initTinyMCE(context) {
    $('textarea.mce_editable', context).each(function() {
      var el = $(this),
          config = $.parseJSON(el.attr('data-mce-config'));

      // not the nicest way to put this here as usuall kittens will die
      // and ponies stop flying
      //
      // only relevant to tiles
      if (el.parents('form#add_tile').size() === 1 ||
          el.parents('form#edit_tile').size() === 1) {

        // filter out buttons we dont allow
        var buttons = [];
        $.each(config.buttons, function(i, button) {
          // probably it would be nice that the list of buttons below would be
          // possible to configure
          if ($.inArray(button, ["style", "bold", "italic", "justifyleft",
              "justifycenter", "justifyright", "justifyfull", "bullist",
              "numlist", "definitionlist", "outdent", "indent", "link",
              "unlink", "code"]) !== -1) {
              // not sure about "anchor", "fullscreen"
              buttons.push(button);
          }
        });
        config.buttons = buttons;
        config.theme_advanced_buttons1 = buttons.join(',');
        config.theme_advanced_buttons2 = '';
        config.theme_advanced_buttons3 = '';

        // copy css from top frame to content frame of tinymce
        // FIXME: its not copying style elements with css using @import
        var content_css = [];
        $('link,style', window.parent.document).each(function(i, item) {
          if ($.nodeName(item, 'link') && $(item).attr('href')) {
            content_css += ',' + $(item).attr('href');
          } else if ($.nodeName(item, 'style') && $(item).attr('src')) {
            content_css += ',' + $(item).attr('src');
          }
        });
        config.content_css = content_css;

        // max height is 8 rows
        el.attr('rows', '8');

      }

      // make initialization work in bootstrap modal
      var modal = el.parents('.modal');
      if (modal.size() !== 0) {

        modal.on('shown', function() {
          el.tinymce(config);
        });
        modal.on('hide', function() {
          tinyMCE.execCommand('mceRemoveControl', false, el.attr('id'));
        });

      // initialize tinymce outside modal
      } else {
        el.tinymce(config);
      }

    });

    // set Text Format dropdown untabbable for better UX
    // TODO: find a better way to fix this
    $('#text_text_format', context).attr('tabindex', '-1');
  }
  if ($.plone && $.plone.init) {
    $.plone.init.register(initTinyMCE);
  } else {
    initTinyMCE(document);
  }

});
"""


class TinyMCECompressorView(BrowserView):
    """ Bundle TinyMCE editor and all resources """

    implements(ITinyMCECompressor)

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
            return TINY_MCE_GZIP

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
