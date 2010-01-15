/**
 * Plone inline styles plugin.
 *
 * @author Rob Gietema
 */

(function() {
    tinymce.create('tinymce.plugins.PloneInlineStylesPlugin', {
        init : function(ed, url) {

            ed.onPreProcess.add(function(ed, o) {

                // Regular Expression to find valid substrings in style attributes
                valid = new RegExp ('('+ed.getParam ('valid_inline_styles').replace (/,/g, '|')+')[a-z\-]*:[^;]*', 'igm');

                // remove all invalid styles, remove empty style attributes (not supported by IE 5.0 Mac)
                tinymce.each(ed.dom.select('*', o.node).reverse(), function(n) {

                    // get style if there is such an Attribute
                    styleAttr = (n.getAttribute('style')) ? n.getAttribute('style') : '';

                    // deal with IE style object, convert to lowercase
                    style = (ed.isMSIE && styleAttr !== '') ? styleAttr.cssText.toLowerCase() : styleAttr.toLowerCase();

                    // get valid styles
                    validStyles = style.match (valid);

                    // reset style
                    style = '';

                    // append valid styles to styles
                    if (validStyles) {
                         for (j=0; j<validStyles.length; j++) {
                              style += validStyles[j] + '; ';
                         }
                    }

                    // if there are valid styles, set style attribute
                    if (style.length > 0) {
                        ed.dom.setAttrib (n, 'style', style);
                    } else {
                        ed.dom.setAttrib (n, 'style', '');
                    }
                });
            });
        },

        getInfo : function() {
            return {
                longname : 'Plone inline styles',
                author : 'Rob Gietema',
                authorurl : 'http://plone.org',
                infourl : 'http://plone.org/products/tinymce',
                version : tinymce.majorVersion + "." + tinymce.minorVersion
            };
        }
    });

    // Register plugin
    tinymce.PluginManager.add('ploneinlinestyles', tinymce.plugins.PloneInlineStylesPlugin);
})();