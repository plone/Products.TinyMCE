/**
 * Plone style plugin
 *
 * @author Four Digits
 */
(function() {
    tinymce.create('tinymce.plugins.PloneStylePlugin', {

        _previousNode       : null,
        _styles             : null,
        _control            : null,

        init : function(ed, url) {
            this._init(ed, url);
        },

        _init : function(ed, url) {
            var t = this;

            // Get styles
            this._styles = eval(ed.getParam('theme_advanced_styles'));

            // Register commands
            ed.addCommand('mceSetStyle', function(ui, v) {
                t._execCommand(ed, v, t._styles);
            });

            ed.onNodeChange.add(this._nodeChange, this);
        },

        _execCommand : function(ed, v, styles) {
            if (e = ed.selection.getNode()) {
                if (v == '-')
                    return;

                function ReplaceTag (curelm, newtag) {
                    if (curelm.nodeName.toLowerCase() != newtag) {
                        // changing to a different node type
                        var newelm;

                        if (((curelm.nodeName.toLowerCase() == "td") || (curelm.nodeName.toLowerCase() == "th")) &&
                            ((newtag != "td") && (newtag != "th"))) {
                            newelm = ed.getDoc().createElement(curelm.nodeName);
                            var child = newelm.appendChild(ed.getDoc().createElement(newtag));
                            for (var c=0; c<curelm.childNodes.length; c++)
                                child.appendChild(curelm.childNodes[c].cloneNode(1));

                            for (var a=0; a<curelm.attributes.length; a++)
                                ed.dom.setAttrib(newelm, curelm.attributes[a].name, ed.dom.getAttrib(e, curelm.attributes[a].name));
                        } else {
                            newelm = ed.getDoc().createElement(newtag);
                            for (var c=0; c<curelm.childNodes.length; c++)
                                newelm.appendChild(curelm.childNodes[c].cloneNode(1));

                            for (var a=0; a<curelm.attributes.length; a++)
                                ed.dom.setAttrib(newelm, curelm.attributes[a].name, ed.dom.getAttrib(e, curelm.attributes[a].name));
                        }

                        b = ed.selection.getBookmark();
                        curelm.parentNode.replaceChild(newelm, curelm);
                        ed.selection.moveToBookmark(b);
                        curelm = newelm;
                    }
                    return curelm;
                }

                var tag = styles[parseInt(v)].tag, className = styles[parseInt(v)].className;

                switch (styles[parseInt(v)].type) {
                    case "Text":
                    case "Print":
                        if ((tag == "") && (className == "")) {
                            ed.execCommand('RemoveFormat', false, null);
                        } else {
                            if (e.nodeName.toLowerCase() != "body") {
                                if (e.tagName.toLowerCase() != tag.toLowerCase()) {
                                    e = ReplaceTag (e, tag);
                                }
                                if (className != "") {
                                    var classnames = ed.dom.getAttrib(e, 'class').split(' ');
                                    var newclassnames = new Array();
                                    newclassnames.push(className)
                                    for (var i = 0; i < classnames.length; i++) {
                                        if ((classnames[i] == 'image-left') ||
                                            (classnames[i] == 'image-right') ||
                                            (classnames[i] == 'image-inline') ||
                                            (classnames[i] == 'captioned')) {
                                            newclassnames.push(classnames[i]);
                                        }
                                    }
                                    e.className = newclassnames.join(' ');
                                }
                            }
                        }
                        break;
                    case "Tables":
                        var n;
                        switch (tag) {
                            case "th":
                            case "td":
                                if (n = this._getParentNode(e,["th","td"])) {
                                    n = ReplaceTag (n, tag);
                                    n.className = className;
                                }
                                break;
                            case "tr":
                                if (n = this._getParentNode(e,["tr"])) {
                                    n.className = className;
                                }
                                break;
                            case "table":
                                if (n = this._getParentNode(e,["table"])) {
                                    n.className = className;
                                }
                                break;
                        }
                        break;
                    case "Lists":
                        if (tag == "dd" || tag == "dt") {
                            e = ReplaceTag(e, tag);
                        } else {
                            var n = this._getParentNode(e,["ol","ul"]);

                            n.className = className;
                        }
                        break;
                    case "Selection":
                        ed.execCommand('mceSetCSSClass', false, className);
                        break;
                }
                ed.nodeChanged();
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

            this._rebuildListBox(ed, n);
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

        _rebuildListBox : function(ed, n) {
            if (this._control == null)
                return;

            // Remove existing items
            this._control.items = [];

            // Set old ID
            this._control.oldID = null;

            // Select nothing
            this._control.select();

            // Check if inside table
            var t = this._getParentNode (n, ["td", "th"]);

            // Check if inside list
            var ul = this._getParentNode (n, ["ul"]);
            var ol = this._getParentNode (n, ["ol"]);
            var dl = this._getParentNode (n, ["dl"]);

            // Fill the listbox
            for (var i = 0; i < this._styles.length; i++) {

                tag = this._styles[i].tag;
                if ((((tag != "td") && (tag != "th") && (tag != "tr") && (tag != "table")) || t) &&
                    (tag != "ul" || ul) &&
                    (tag != "ol" || ol) &&
                    (((tag != "dl") && (tag != "dd") && (tag != "dt")) || dl)) {

                    // Add item
                    this._control.add(
                        this._styles[i].title,
                        this._styles[i].className == '-' ? '-' : i,
                        {'class' : this._styles[i].className == '-' ? 'mceMenuItemTitle' : 'mce_formatPreview mce_' + this._styles[i].tag}
                    );

                    var p = this._getParentNode(n, ["th","td","p","h1","h2","h3","h4","h5","h6","pre","div","span","blockquote","samp","code", "ul", "ol","dl","img"]);
                    var il = false;
                    if (p && (p.nodeName.toLowerCase() == "ul" || p.nodeName.toLowerCase() == "ol")) {
                        var lc = ed.dom.getAttrib(p, "class");

                        if (lc == this._styles[i].className) {
                            il = true;
                        }
                    } else if (p && p.nodeName.toLowerCase() == "dl") {
                        var d = this._getParentNode(n, ["dd","dt"]);
                        if (d && d.nodeName.toLowerCase() == tag) {
                            il = true;
                            p = d;
                        }
                    } else {
                        il = true;
                    }
                    if (p && (p.nodeName.toLowerCase() == this._styles[i].tag) && (p.className.indexOf(this._styles[i].className) != -1) && il) {
                        this._control.select(i);
                    }
                }
            }

            if (this._control.menu) {
                tinymce.DOM.remove("menu_" + this._control.menu.id);
            }
            this._control.renderMenu();
        },

        createControl : function(n, cm) {
            if (n == 'style') {
                this._control = cm.createListBox('style_' + tinyMCE.activeEditor.id, {
                    title    : 'Style...',
                    cmd        : 'mceSetStyle'
                });
                return this._control;
            }
            
            return null;
        },

        getInfo : function() {
            return {
                longname : 'Plone style',
                author : 'Rob Gietema',
                authorurl : 'http://plone.org',
                infourl : 'http://plone.org/products/tinymce',
                version : tinymce.majorVersion + "." + tinymce.minorVersion
            };
        }
    });

    // Register plugin
    tinymce.PluginManager.add('plonestyle', tinymce.plugins.PloneStylePlugin);
})();
