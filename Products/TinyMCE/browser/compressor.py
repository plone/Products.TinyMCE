"""
Based on "TinyMCE Compressor PHP" from MoxieCode.

http://tinymce.moxiecode.com/

Copyright (c) 2008 Jason Davies
Licensed under the terms of the MIT License (see LICENSE.txt)
"""

from datetime import datetime
from cStringIO import StringIO

import zope.component
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.ResourceRegistries.tools.packer import JavascriptPacker

from Products.TinyMCE.interfaces.utility import ITinyMCE

def split_commas(str):
    return not str and [] or str.split(",")

def getplugins(config):
    plugins = "pagebreak,table,save,advhr,emotions,insertdatetime,preview,media,searchreplace,print,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,inlinepopups,plonestyle,tabfocus,definitionlist,ploneinlinestyles"
    sp = config['libraries_spellchecker_choice']
    sp = sp != "browser" and sp or ""
    if sp:
        plugins += ',' + sp;

    for plugin in config['customplugins']:
        if '|' not in plugin:
            plugins += ',' + plugin
        else:
            plugins += ',' + plugin.split('|')[0]

    if config['contextmenu']:
        plugins += ',contextmenu'

    if config['autoresize']:
        plugins += ',autoresize'
    return plugins

def getstyles(config):

        h = {'Text': [], 'Selection': [], 'Tables': [], 'Lists': [], 'Print': []}
        styletype = ""

        # Push title
        h['Text'].append('{ title: "Text", tag: "", className: "-", type: "Text" }')
        h['Selection'].append('{ title: "Selection", tag: "", className: "-", type: "Selection" }')
        h['Tables'].append('{ title: "Tables", tag: "table", className: "-", type: "Tables" }')
        h['Lists'].append('{ title: "Lists", tag: "ul", className: "-", type: "Lists" }')
        h['Lists'].append('{ title: "Lists", tag: "ol", className: "-", type: "Lists" }')
        h['Lists'].append('{ title: "Lists", tag: "dl", className: "-", type: "Lists" }')
        h['Print'].append('{ title: "Print", tag: "", className: "-", type: "Print" }')

        # Add defaults
        h['Text'].append('{ title: "' + config['labels']['label_paragraph'] + '", tag: "p", className: "", type: "Text" }')
        h['Selection'].append('{ title: "' + config['labels']['label_styles'] + '", tag: "", className: "", type: "Selection" }')
        h['Tables'].append('{ title: "'+config['labels']['label_plain_cell'] +'", tag: "td", className: "", type: "Tables" }')
        h['Lists'].append('{ title: "'+config['labels']['label_lists'] +'", tag: "dl", className: "", type: "Lists" }')

        for i in config['styles']:
            e = i.split('|')
            if len(e) <= 2:
                e[2] = ""
            if e[1].lower() in ('del', 'ins', 'span'):
                    styletype = "Selection"
            elif e[1].lower() in ('table', 'tr', 'td', 'th'):
                    styletype = "Tables"
            elif e[1].lower() in ('ul', 'ol', 'li', 'dt', 'dd', 'dl'):
                    styletype = "Lists"
            else:
                    styletype = "Text"

            if e[2] == "pageBreak":
                    styletype = "Print"
            h[styletype].append('{ title: "' + e[0] + '", tag: "' + e[1] + '", className: "' + e[2] + '", type: "' + styletype + '" }')

            # Add items to list
            a = []
            if len(h['Text']) > 1:
                a.extend(h['Text'])
            if len(h['Selection']) > 1:
                a.extend(h['Selection'])
            if len(h['Tables']) > 1:
                a.extend(h['Tables'])
            if len(h['Lists']) > 1:
                a.extend(h['Lists'])
            if len(h['Print']) > 1:
                a.extend(h['Print'])

            return '[' + ','.join(a) + ']'

def getlabels(config):
    return str(dict([(key, val.encode('utf-8')) for key, val in config['labels'].iteritems()]))

BUTTON_WIDTHS = {'style': 150, 'forecolor': 32, 'backcolor': 32, 'tablecontrols': 285}

def gettoolbars(config):

    t = [[], [], [], []]
    cur_toolbar = 0
    cur_x = 0

    for i in config['buttons']:
        button_width = BUTTON_WIDTHS.get(i, 23)
        if cur_x + button_width > config['toolbar_width']:
            cur_x = button_width
            cur_toolbar += 1
        else:
            cur_x += button_width;
        if cur_toolbar <= 3:
            t[cur_toolbar].append(i)

    return [','.join(t[0]), ','.join(t[1]), ','.join(t[2]), ','.join(t[3])]

def getvalidelements(config):
        a = []
        valid_elements = config['valid_elements']

        for valid_element in valid_elements:
            s = valid_element
            if (valid_elements[valid_element]):
                s += '[' + '|'.join(valid_elements[valid_element]) + ']'
            a.append(s)
        return ','.join(a)

class TinyMCECompressorView(BrowserView):

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
        portal_url = plone_portal_state.portal_url()
        base_url = '/'.join([self.context.absolute_url(), self.__name__])

        if not isJS:
            utility = zope.component.queryUtility(ITinyMCE)
            config = utility.getConfiguration(context=self.context,
                                              request=self.request, as_json=False)
            plugins = getplugins(config)

            tiny_mce_gzip = self.tiny_mce_gzip(base_url=base_url,
                                      config=config,
                                      portal_url=portal_url,
                                      plugins=getplugins(config),
                                      styles=getstyles(config),
                                      labels=getlabels(config),
                                      valid_elements=getvalidelements(config),
                                      toolbars=gettoolbars(config))
            return JavascriptPacker('full').pack(tiny_mce_gzip)

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
        return ''.join(content)
