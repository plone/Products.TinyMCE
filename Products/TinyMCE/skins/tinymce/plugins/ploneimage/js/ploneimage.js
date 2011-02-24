var ImageDialog = {
    current_path : "",
    current_link : "",
    current_url : "",
    current_class : "",
    labels : "",
    
    preInit : function() {
        var url;

        tinyMCEPopup.requireLangPack();

        if (url = tinyMCEPopup.getParam("external_image_list_url"))
            document.write('<script language="javascript" type="text/javascript" src="' + tinyMCEPopup.editor.documentBaseURI.toAbsolute(url) + '"></script>');
    },

    init : function() {
        var f0 = document.forms[0];
        var f1 = document.forms[1];
        var f2 = document.forms[2];
        var nl0 = f0.elements;
        var nl1 = f1.elements;
        var nl2 = f2.elements;
        var ed = tinyMCEPopup.editor;
        var dom = ed.dom;
        var n = ed.selection.getNode();
        labels = eval(ed.getParam('labels'));

        tinyMCEPopup.resizeToInnerSize();

        if (!ed.settings.allow_captioned_images) {
            document.getElementById ('caption').parentNode.parentNode.style.display = 'none';
        }

        // Check if rooted
        if (ed.settings.rooted) {
            document.getElementById('home').style.display = 'none';
        }

        if (n.nodeName == 'IMG') {
            var href = dom.getAttrib(n, 'src');
            if (href.indexOf('/')) {
                var href_array = href.split('/');
                var last = href_array[href_array.length-1];
                var pos = href.indexOf('@@images/image/');
                if (last.indexOf('image_') != -1) {
                    var dimensions = '@@images/image/' + href_array.pop().substring(6);
                    selectByValue(f0, 'dimensions', dimensions, true);
                    href = href_array.join ('/');
                } else if (pos != -1) {
                    var dimensions = href.substring(pos);
                    selectByValue(f0, 'dimensions', dimensions, true);
                    href = href.substring(0, pos - 1);
                }
            }
            var classnames = dom.getAttrib(n, 'class').split(' ');
            var classname = "";
            for (var i = 0; i < classnames.length; i++) {
                if (classnames[i] == 'captioned') {
                    if (tinyMCEPopup.editor.settings.allow_captioned_images) {
                        f0.caption.checked = true;
                    }
                } else if ((classnames[i] == 'image-inline') ||
                           (classnames[i] == 'image-left') ||
                           (classnames[i] == 'image-right')) {
                    classname = classnames[i];
                } else {
                    ImageDialog.current_class = classnames[i];
                }
            }
            selectByValue(f0, 'classes', classname, true);
            nl2.insert.value = ed.getLang('update');


            if (href.indexOf('resolveuid') != -1) {
                var current_uid = href.split('resolveuid/')[1];
                tinymce.util.XHR.send({
                    url : tinyMCEPopup.editor.settings.portal_url + '/portal_tinymce/tinymce-getpathbyuid?uid=' + current_uid,
                    type : 'GET',
                    success : function(text) {
                        ImageDialog.current_url = ImageDialog.getAbsoluteUrl(tinyMCEPopup.editor.settings.document_base_url, text);
                        if (tinyMCEPopup.editor.settings.link_using_uids) {
                            ImageDialog.current_link = href;
                        } else {
                            ImageDialog.current_link = ImageDialog.current_url;
                        }
                        ImageDialog.getFolderListing(ImageDialog.getParentUrl(ImageDialog.current_url), 'tinymce-jsonimagefolderlisting');
                    }
                });
            } else {
                href = this.getAbsoluteUrl(tinyMCEPopup.editor.settings.document_base_url, href);
                this.current_link = href;
                this.getFolderListing(this.getParentUrl(href), 'tinymce-jsonimagefolderlisting');
            }
        } else {
            this.getCurrentFolderListing();
        }
    },

    insert : function() {
        var ed = tinyMCEPopup.editor, t = this, f = document.forms[0];
        var href = this.getRadioValue('internallink', 0);

        if (href === '') {
            if (ed.selection.getNode().nodeName == 'IMG') {
                ed.dom.remove(ed.selection.getNode());
                ed.execCommand('mceRepaint');
            }

            tinyMCEPopup.close();
            return;
        }

        t.insertAndClose();
    },

    insertAndClose : function() {
        var ed = tinyMCEPopup.editor;
        var f0 = document.forms[0];
        var f1 = document.forms[1];
        var f2 = document.forms[2];
        var nl0 = f0.elements;
        var nl1 = f1.elements;
        var nl2 = f2.elements;
        var v;
        var args = {};
        var el;

        tinyMCEPopup.restoreSelection();

        // Fixes crash in Safari
        if (tinymce.isWebKit)
            ed.getWin().focus();
            
        var href = this.getRadioValue('internallink', 0);
        var dimensions = this.getSelectValue(f0, 'dimensions');
        if (dimensions != "") {
            href += '/' + dimensions;
        }
        args = {
            src : href,
            'class' : this.getSelectValue(f0, 'classes') +
                ((ed.settings.allow_captioned_images && f0.elements['caption'].checked) ? ' captioned' : '') +
                (ImageDialog.current_class == '' ? '' : ' ' + ImageDialog.current_class)
        };

        el = ed.selection.getNode();

        if (el && el.nodeName == 'IMG') {
            ed.dom.setAttribs(el, args);
        } else {
            ed.execCommand('mceInsertContent', false, '<img id="__mce_tmp" />', {skip_undo : 1});
            ed.dom.setAttribs('__mce_tmp', args);
            ed.dom.setAttrib('__mce_tmp', 'id','');
            ed.undoManager.add();
        }

        var description_href = nl0.description_href.value;
        var description = nl0.description.value;
        var data = "description=" + encodeURIComponent(description);
        tinymce.util.XHR.send({
            url : description_href + '/tinymce-setDescription',
            content_type : "application/x-www-form-urlencoded",
            type : "POST",
            data : data
        });

        tinyMCEPopup.close();
    },

    checkSearch : function(e) {
        if (document.getElementById('searchtext').value.length >= 3 && (tinyMCEPopup.editor.settings.livesearch || e.keyCode == 13)) {
            ImageDialog.getFolderListing(tinyMCEPopup.editor.settings.navigation_root_url, 'tinymce-jsonimagesearch');
        } 
    },

    getAttrib : function(e, at) {
        var ed = tinyMCEPopup.editor, dom = ed.dom, v, v2;

        if (ed.settings.inline_styles) {
            switch (at) {
                case 'align':
                    if (v = dom.getStyle(e, 'float'))
                        return v;

                    if (v = dom.getStyle(e, 'vertical-align'))
                        return v;

                    break;

                case 'hspace':
                    v = dom.getStyle(e, 'margin-left')
                    v2 = dom.getStyle(e, 'margin-right');

                    if (v && v == v2)
                        return parseInt(v.replace(/[^0-9]/g, ''));

                    break;

                case 'vspace':
                    v = dom.getStyle(e, 'margin-top')
                    v2 = dom.getStyle(e, 'margin-bottom');
                    if (v && v == v2)
                        return parseInt(v.replace(/[^0-9]/g, ''));

                    break;

                case 'border':
                    v = 0;

                    tinymce.each(['top', 'right', 'bottom', 'left'], function(sv) {
                        sv = dom.getStyle(e, 'border-' + sv + '-width');

                        // False or not the same as prev
                        if (!sv || (sv != v && v !== 0)) {
                            v = 0;
                            return false;
                        }

                        if (sv)
                            v = sv;
                    });

                    if (v)
                        return parseInt(v.replace(/[^0-9]/g, ''));

                    break;
            }
        }

        if (v = dom.getAttrib(e, at))
            return v;

        return '';
    },

    setSwapImage : function(st) {
        var f = document.forms[0];

        f.onmousemovecheck.checked = st;
        setBrowserDisabled('overbrowser', !st);
        setBrowserDisabled('outbrowser', !st);

        if (f.over_list)
            f.over_list.disabled = !st;

        if (f.out_list)
            f.out_list.disabled = !st;

        f.onmouseoversrc.disabled = !st;
        f.onmouseoutsrc.disabled  = !st;
    },

    fillClassList : function(id) {
        var dom = tinyMCEPopup.dom, lst = dom.get(id), v, cl;

        if (v = tinyMCEPopup.getParam('theme_advanced_styles')) {
            cl = [];

            tinymce.each(v.split(';'), function(v) {
                var p = v.split('=');

                cl.push({'title' : p[0], 'class' : p[1]});
            });
        } else
            cl = tinyMCEPopup.editor.dom.getClasses();

        if (cl.length > 0) {
            lst.options[lst.options.length] = new Option(tinyMCEPopup.getLang('not_set'), '');

            tinymce.each(cl, function(o) {
                lst.options[lst.options.length] = new Option(o.title || o['class'], o['class']);
            });
        } else
            dom.remove(dom.getParent(id, 'tr'));
    },

    fillFileList : function(id, l) {
        var dom = tinyMCEPopup.dom, lst = dom.get(id), v, cl;

        l = window[l];

        if (l && l.length > 0) {
            lst.options[lst.options.length] = new Option('', '');

            tinymce.each(l, function(o) {
                lst.options[lst.options.length] = new Option(o[0], o[1]);
            });
        } else
            dom.remove(dom.getParent(id, 'tr'));
    },

    changeAppearance : function() {
        var ed = tinyMCEPopup.editor, f = document.forms[0], img = document.getElementById('alignSampleImg');

        if (img) {
            if (ed.getParam('inline_styles')) {
                ed.dom.setAttrib(img, 'style', f.style.value);
            } else {
                img.align = f.align.value;
                img.border = f.border.value;
                img.hspace = f.hspace.value;
                img.vspace = f.vspace.value;
            }
        }
    },

    changeHeight : function() {
        var f = document.forms[0], tp, t = this;

        if (!f.constrain.checked || !t.preloadImg) {
            return;
        }

        if (f.width.value == "" || f.height.value == "")
            return;

        tp = (parseInt(f.width.value) / parseInt(t.preloadImg.width)) * t.preloadImg.height;
        f.height.value = tp.toFixed(0);
    },

    changeWidth : function() {
        var f = document.forms[0], tp, t = this;

        if (!f.constrain.checked || !t.preloadImg) {
            return;
        }

        if (f.width.value == "" || f.height.value == "")
            return;

        tp = (parseInt(f.height.value) / parseInt(t.preloadImg.height)) * t.preloadImg.width;
        f.width.value = tp.toFixed(0);
    },

    changeMouseMove : function() {
    },

    setFormValue : function(name, value, formnr) {
        document.forms[formnr].elements[name].value = value;
    },
    
    getInputValue : function(name, formnr) {
        return document.forms[formnr].elements[name].value;
    },

    getRadioValue : function(name, formnr) {
        var value = "";
        var elm = document.forms[formnr][name];
        if (typeof (elm) != 'undefined') {
            if (typeof(elm.value) == 'undefined') {
                for (var i = 0; i < elm.length; i++) {
                    if (elm[i].checked) {
                        value = elm[i].value;
                    }
                }
            } else {
                if (elm.checked) {
                    value = elm.value;
                }
            }
        }

        return value;
    },

    setRadioValue : function(name, value, formnr) {
        var elm = document.forms[formnr][name];
        if (typeof (elm) != 'undefined') {
            if (typeof(elm['value']) == 'undefined') {
                for (var i = 0; i < elm.length; i++) {
                    if (elm[i].value == value) {
                        elm[i].checked = true;
                    }
                }
            } else {
                if (elm.value == value) {
                    elm.checked = true;
                }
            }
        }
    },
    
    getSelectValue : function(form_obj, field_name) {
        var elm = form_obj.elements[field_name];

        if (elm == null || elm.options == null)
            return "";

        return elm.options[elm.selectedIndex].value;
    },

    setDetails : function(path,title) {
        // Sends a low level Ajax request
        tinymce.util.XHR.send({
            url : path + '/tinymce-jsondetails',
            type : 'POST',
            success : function(text) {
                var html = "";
                var data = eval('(' + text + ')');
                var f0 = document.forms[0];
                var elm = f0.elements['dimensions'];
                var dimension = "";
                if (elm != null && elm.options != null) {
                    dimension = elm.options[elm.selectedIndex].value;
                }

                if (data.thumb == "") {
                    document.getElementById ('previewimagecontainer').innerHTML = data.description;
                } else {
                    document.getElementById ('previewimagecontainer').innerHTML = '<img src="' + data.thumb + '" border="0" />';
                }
                document.getElementById('description').value = data.description;
                document.getElementById('description_href').value = path;
                if (data.scales) {
                    var dimensions = document.getElementById('dimensions');
                    var newdimensions = [];
                    dimensions.innerHTML='';
                    for(var i=0; i<data.scales.length; i++) {
                        var nd = document.createElement('option');
                        nd.value = data.scales[i].value;
                        if (nd.value == dimension) {
                            nd.selected = true;
                        }
                        if (data.scales[i].size[0]) {
                            nd.text = data.scales[i].title+' ('+data.scales[i].size[0]+'x'+data.scales[i].size[1]+')';
                        } else {
                            nd.text = data.scales[i].title;
                        }
                        dimensions.options.add(nd);
                    }
                }
                this.current_path = path;
                document.getElementById('internal_details_panel').style.display = 'block';
                document.getElementById('upload_panel').style.display = 'none';
            }
        });
    },

    getCurrentFolderListing : function() {
        this.getFolderListing(tinyMCEPopup.editor.settings.document_base_url, 'tinymce-jsonimagefolderlisting');
    },
    
    getFolderListing : function(path, method) {
        // Sends a low level Ajax request
        tinymce.util.XHR.send({
            url : path + '/' + method,
            content_type : "application/x-www-form-urlencoded",
            type : 'POST',
            data : "searchtext=" + document.getElementById('searchtext').value + "&rooted=" + (tinyMCEPopup.editor.settings.rooted ? "True" : "False") + "&document_base_url=" + encodeURIComponent(tinyMCEPopup.editor.settings.document_base_url),
            success : function(text) {
                var html = "";
                var data = eval('(' + text + ')');
                if (data.items.length == 0) {
                    html = labels['label_no_items'];
                } else {
                    for (var i = 0; i < data.items.length; i++) {
                        if (data.items[i].url == ImageDialog.current_link && tinyMCEPopup.editor.settings.link_using_uids) {
                            ImageDialog.current_link = 'resolveuid/' + data.items[i].uid;
                        }
                        html += '<div class="' + (i % 2 == 0 ? 'even' : 'odd') + '">';
                        if (data.items[i].is_folderish) {
                            if (data.items[i].icon.length) {
                                html += '<img src="' + data.items[i].icon + '" border="0" style="margin-left: 17px" /> ';
                            }
                            html += '<a class="contenttype-' + data.items[i].normalized_type + '" ';
                            html += 'href="javascript:ImageDialog.getFolderListing(\'' + data.items[i].url + '\',\'tinymce-jsonimagefolderlisting' + '\')">';
                            html += data.items[i].title;
                            html += '</a>';
                        } else {
                            html += '<input onclick="ImageDialog.setDetails(\'';
                            html += data.items[i].url + '\',\'' + data.items[i].title.replace(/'/g, "\\'") + '\');"';
                            html += ' type="radio" class="noborder" name="internallink" value="';
                            if (tinyMCEPopup.editor.settings.link_using_uids) {
                                html += "resolveuid/" + data.items[i].uid;
                            } else {
                                html += data.items[i].url;
                            }
                            html += '"/> ';
                            if (data.items[i].icon.length) {
                                html += '<img src="' + data.items[i].icon + '" border="0"/> ';
                            }
                            html += '<span class="contenttype-' + data.items[i].normalized_type + '">' + data.items[i].title + '</span>';
                        }
                        html += '</div>';
                    }
                }
                document.getElementById ('internallinkcontainer').innerHTML = html;
                if (data.parent_url == "") {
                    document.getElementById ('uponelevel').style.display = 'none';
                    document.getElementById ('uponelevel').href = 'javascript:void(0)';
                } else {
                    document.getElementById ('uponelevel').style.display = 'block';
                    document.getElementById ('uponelevel').href = 'javascript:ImageDialog.getFolderListing(\'' + data.parent_url + '\',\'tinymce-jsonimagefolderlisting' + '\')';
                }

                html = "";
                for (var i = 0; i < data.path.length; i++) {
                    if (i != 0) {
                        html += " &rarr; ";
                    }
                    if (i == data.path.length - 1) {
                        html += data.path[i].title;
                    } else {
                        html += '<a href="javascript:ImageDialog.getFolderListing(\'' + data.path[i].url + '\',\'tinymce-jsonimagefolderlisting' + '\')">';
                        html += data.path[i].title;
                        html += '</a>';
                    }
                }
                document.getElementById ('internalpath').innerHTML = html;

                // Check if allowed to upload
                if (data.upload_allowed) {
                    document.getElementById ('upload').style.display = '';
                } else {
                    document.getElementById ('upload').style.display = 'none';
                }

                // Set global path
                ImageDialog.current_path = path;
                document.forms[1].action = ImageDialog.current_path + '/tinymce-upload';
                ImageDialog.setRadioValue('internallink', ImageDialog.current_link, 0);

                if (ImageDialog.current_link != "") {
                    if (ImageDialog.current_link.indexOf('resolveuid') != -1) {
                        current_uid = ImageDialog.current_link.split('resolveuid/')[1];
                        tinymce.util.XHR.send({
                            url : tinyMCEPopup.editor.settings.portal_url + '/portal_tinymce/tinymce-getpathbyuid?uid=' + current_uid,
                            type : 'GET',
                            success : function(text) {
                                ImageDialog.current_url = ImageDialog.getAbsoluteUrl(tinyMCEPopup.editor.settings.document_base_url, text);
                                ImageDialog.setDetails(ImageDialog.current_url,'');
                            }
                        });
                    } else {
                        ImageDialog.setDetails(ImageDialog.current_link,'');
                    }
                }
            }
        });
    },

    getParentUrl : function(url) {
        var url_array = url.split('/');
        url_array.pop();
        return url_array.join('/');
    },

    getAbsoluteUrl : function(base, link) {
        if ((link.indexOf('http://') != -1) || (link.indexOf('https://') != -1) || (link.indexOf('ftp://') != -1)) {
            return link;
        }
    
        var base_array = base.split('/');
        var link_array = link.split('/');
    
        // Remove document from base url
        base_array.pop();
    
        while (link_array.length != 0) {
            var item = link_array.shift();
            if (item == ".") {
                // Do nothing
            } else if (item == "..") {
                // Remove leave node from base
                base_array.pop();
            } else {
                // Push node to base_array
                base_array.push(item);
            }
        }
        return (base_array.join('/'));
    },

    displayPanel : function(elm_id) {
        document.getElementById ('internal_panel').style.display = elm_id == 'internal_panel' || elm_id == 'upload_panel' ? 'block' : 'none';
        document.getElementById ('internal_details_panel').style.display = elm_id == 'internal_panel' ? 'block' : 'none';
        document.getElementById ('upload_panel').style.display = elm_id == 'upload_panel' ? 'block' : 'none';
    }
};

function uploadOk(ok_msg) {
    ImageDialog.current_link = ok_msg;
    ImageDialog.displayPanel('internal_panel');
    ImageDialog.getFolderListing(ImageDialog.current_path, 'tinymce-jsonimagefolderlisting');
}

function uploadError(error_msg) {
    alert (error_msg);
}

ImageDialog.preInit();
tinyMCEPopup.onInit.add(ImageDialog.init, ImageDialog);
