/**
 * @author Rob Gietema
 * @copyright Copyright © 2009, Four Digits, All rights reserved.
 */

(function() {
    // Load plugin specific language pack
    //tinymce.PluginManager.requireLangPack('flags');

    tinymce.create('tinymce.plugins.DefinitionList', {

        _previousNode       : null,

        /**
         * Initializes the plugin, this will be executed after the plugin has been created.
         * This call is done before the editor instance has finished it's initialization so use the onInit event
         * of the editor instance to intercept that event.
         *
         * @param {tinymce.Editor} ed Editor instance that the plugin is initialized in.
         * @param {string} url Absolute URL to where the plugin is located.
         */
        init : function(ed, url) {
            var t = this;

            // Register commands
            ed.addCommand('mceInsertDefinitionList', function(ui, v) {
                t._execCommand(ed, v);
            });

            // Register flags button
            ed.addButton('definitionlist', {
                title : 'Definition list',
                cmd : 'mceInsertDefinitionList',
                image : url + '/img/definitionlist.gif'
            });

            ed.onNodeChange.add(this._nodeChange, this);
            ed.onKeyUp.add(this._keyUp, this);
        },

        _execCommand : function(ed, v) {
            function ReplaceTag(curelm, remove) {
                // changing to a different node type
                var newelm;

                if (remove) {
                    b = ed.selection.getBookmark();
                    var html = "";
                    newelm = ed.getDoc().createElement('p');
                    for (var c=0; c<curelm.childNodes.length; c++)
                        html += curelm.childNodes[c].innerHTML + '<br/>';
                    newelm.innerHTML = html;
                    curelm.parentNode.replaceChild(newelm, curelm);
                    ed.selection.moveToBookmark(b);
                } else {
                    var dl = ed.getDoc().createElement('dl');
                    newelm = ed.getDoc().createElement('dt');
                    for (var c=0; c<curelm.childNodes.length; c++)
                        newelm.appendChild(curelm.childNodes[c].cloneNode(1));

                    b = ed.selection.getBookmark();
                    dl.appendChild(newelm);
                    curelm.parentNode.replaceChild(dl, curelm);
                    ed.selection.moveToBookmark(b);
                }
            }

            // Get node and parent blocknode
            var e = ed.selection.getNode();
            var p = this._getParentNode(e, ["p","h1","h2","h3","h4","h5","h6","pre","div","blockquote","samp","code", "ul","ol","dl"]);

            if (p) {
                // Insert definition list
                tag = p.tagName.toLowerCase();
                if (tag == "dl") {
                    ReplaceTag(p, true);
                } else if ((tag != "ol") && (tag != "ul")) {
                    ReplaceTag(p, false);
                }
            }
        },

        _keyUp : function(ed, e) {
            function ReplaceTag(curelm, newtag) {
                // changing to a different node type
                var newelm = ed.getDoc().createElement(newtag);
                b = ed.selection.getBookmark();
                ed.dom.replace(newelm, curelm, true);
                ed.selection.moveToBookmark(b);
            }

            if (e.keyCode == 13) {
                var n = ed.selection.getNode();
                var p = this._getParentNode(n, ["dl"])
                if (p) {
                    var d = this._getParentNode(n, ["dt","dd"]);
                    if (d.tagName.toLowerCase() == "dt") {
//                        ReplaceTag(d, "dd");
                    } else {
//                        ReplaceTag(d, "dt");
                    }
                }
            }
        },

        _nodeChange : function(ed, cm, n) {
            // Check if active editor
            if (tinyMCE.activeEditor.id != ed.id) {
                return;
            }

            // Check if node is the same as previous node
            if (n == this._previousNode) {
                return;
            } else {
                this._previousNode = n;
            }

            // Set button state
            cm.setActive('definitionlist', this._getParentNode(n, ["dl"]));
        },

        _inArray : function(s, a) {
            for (var i=0; i<a.length; i++) {
                if (s == a[i]) {
                    return true;
                }
            }
            return false;
        },

        _getParentNode : function(e, a) {
            a.push("body");
            var p = e;
            while (!this._inArray(p.nodeName.toLowerCase(), a)) {
                p = p.parentNode;
            }
            if (p.nodeName.toLowerCase() == "body") {
                return false;
            } else {
                return p;
            }
        },

        /**
         * Returns information about the plugin as a name/value array.
         * The current keys are longname, author, authorurl, infourl and version.
         *
         * @return {Object} Name/value array containing information about the plugin.
         */
        getInfo : function() {
            return {
                longname : 'Flags',
                author : 'Four Digits',
                authorurl : 'http://www.fourdigits.nl',
                infourl : 'http://plone.org/products/tinymce',
                version : "1.0"
            };
        }
    });

    // Register plugin
    tinymce.PluginManager.add('definitionlist', tinymce.plugins.DefinitionList);
})();