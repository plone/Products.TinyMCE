/*jslint sloppy: true, maxerr: 50, indent: 4 */
/*global tinymce */

/**
 * Plone image plugin based on advimage plugin.
 *
 * @author Rob Gietema
 */

(function () {
    tinymce.create('tinymce.plugins.PloneBrowserPlugin', {
        init : function (ed, url) {
            // Register commands
            ed.addCommand('mcePloneImage', function () {
                // Internal image object like a flash placeholder
                var class_name = ed.dom.getAttrib(ed.selection.getNode(), 'class');
                if (class_name && class_name.indexOf('mceItem') !== -1) {
                    return;
                }

                ed.windowManager.open({
                    file : url + '/plonebrowser.htm?ploneimage=1',
                    width : 820 + parseInt(ed.getLang('plonebrowser.delta_width', 0), 10),
                    height : 500 + parseInt(ed.getLang('plonebrowser.delta_height', 0), 10),
                    inline : 1
                }, {
                    plugin_url : url
                });
            });
            ed.addCommand('mcePloneLink', function() {
                var se = ed.selection;

                // No selection and not in link
                if (se.isCollapsed() && !ed.dom.getParent(se.getNode(), 'A'))
                    return;

                ed.windowManager.open({
                    file : url + '/plonebrowser.htm?plonelink=1',
                    width : 820 + parseInt(ed.getLang('plonebrowser.delta_width', 0)),
                    height : 540 + parseInt(ed.getLang('plonebrowser.delta_height', 0)),
                    inline : 1
                }, {
                    plugin_url : url
                });
            });

            // Register buttons
            ed.addButton('image', {
                title : 'advanced.image_desc',
                cmd : 'mcePloneImage'
            });
            ed.addButton('link', {
                title : 'advanced.link_desc',
                cmd : 'mcePloneLink'
            });

            ed.addShortcut('ctrl+k', 'advanced.link_desc', 'mcePloneLink');

            // disable link plugin if not selection or anchor
            ed.onNodeChange.add(function(ed, cm, n, co) {
                cm.setDisabled('link', co && n.nodeName != 'A');
                cm.setActive('link', n.nodeName == 'A' && !n.name);
            });
        },

        getInfo : function () {
            return {
                longname : 'Plone image',
                author : 'Rob Gietema',
                authorurl : 'http://plone.org',
                infourl : 'http://plone.org/products/tinymce',
                version : tinymce.majorVersion + "." + tinymce.minorVersion
            };
        }
    });

    // Register plugin
    tinymce.PluginManager.add('plonebrowser', tinymce.plugins.PloneBrowserPlugin);
}());
