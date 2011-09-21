var current_path;
var current_link = "";
var current_url = "";
var current_pageanchor = "";

function init() {
    var formGeneralObj = document.forms[0];
    var formUploadObj = document.forms[1];
    var formAdvancedObj = document.forms[2];
    var formButtonsObj = document.forms[3];
    var inst = tinyMCEPopup.editor;
    var elm = inst.selection.getNode();
    var html;

    // Check if update or insert
    elm = inst.dom.getParent(elm, "A");
    if (elm != null && elm.nodeName == "A")
        var action = "update";
    else
        var action = "insert";

    if (action == "update") {
        var href = inst.dom.getAttrib(elm, 'href');
        href = tinymce.trim(href)

        // Setup form data
        setFormValue('href', href, 0);
        if ((typeof(elm.title) != "undefined") && (elm.title != "")) {
            setFormValue('title', inst.dom.getAttrib(elm, 'title'), 2);
        }

        if (href.charAt(0) == '#') {
            // Check if anchor
            displayPanel('anchors_panel');
            setRadioValue('anchorlink', href, 0);
        } else if (href.indexOf('mailto:') != -1) {
            // email
            displayPanel('mail_panel');
            var mailaddress = href.split('mailto:')[1];
            var mailsubject = "";

            if (mailaddress.indexOf('?subject=') != -1) {
                mailsubject = mailaddress.split('?subject=')[1];
                mailaddress = mailaddress.split('?subject=')[0];
            }

            setFormValue('mailaddress', mailaddress, 0);
            setFormValue('mailsubject', mailsubject, 0);
        } else if ((href.indexOf('http://') == 0) || (href.indexOf('https://') == 0) || (href.indexOf('ftp://') == 0)) {
            // checkExternalURL
            displayPanel('external_panel');
            if (href.indexOf('http://') == 0) {
                href = href.substr(7,href.length);
                selectByValue(formGeneralObj, 'externalurlprefix', 'http://', true);
                setFormValue('externalurl', href, 0);
            } else if (href.indexOf('https://') == 0) {
                href = href.substr(8,href.length);
                selectByValue(formGeneralObj, 'externalurlprefix', 'https://', true);
                setFormValue('externalurl', href, 0);
            } else if (href.indexOf('ftp://') == 0) {
                href = href.substr(6,href.length);
                selectByValue(formGeneralObj, 'externalurlprefix', 'ftp://', true);
                setFormValue('externalurl', href, 0);
            }
        } else {
            // internal
            if (href.indexOf('#') != -1) {
                current_pageanchor = href.split('#')[1];
                href = href.split('#')[0];
            }
            if (href.indexOf('resolveuid') != -1) {
                current_uid = href.split('resolveuid/')[1];
                tinymce.util.XHR.send({
                    url : tinyMCEPopup.editor.settings.portal_url + '/portal_tinymce/tinymce-getpathbyuid?uid=' + current_uid,
                    type : 'GET',
                    success : function(text) {
                        current_url = getAbsoluteUrl(tinyMCEPopup.editor.settings.document_base_url, text);
                        current_link = href;
                        getFolderListing(getParentUrl(current_url), 'tinymce-jsonlinkablefolderlisting');
                    }
                });
            } else {
                href = getAbsoluteUrl(tinyMCEPopup.editor.settings.document_base_url, href);
                current_link = href;
                getFolderListing(getParentUrl(href), 'tinymce-jsonlinkablefolderlisting');
            }
        }

        selectByValue(formAdvancedObj, 'targetlist', inst.dom.getAttrib(elm, 'target'), true);
    } else {
        href = inst.selection.getContent();
        href = tinymce.trim(href)
        // external
        if ((href.indexOf('http://') == 0) || (href.indexOf('https://') == 0) || (href.indexOf('ftp://') == 0)) {
            displayPanel('external_panel');
            if (href.indexOf('http://') == 0) {
                href = href.substr(7,href.length);
                selectByValue(formGeneralObj, 'externalurlprefix', 'http://', true);
                setFormValue('externalurl', href, 0);
            } else if (href.indexOf('https://') == 0) {
                href = href.substr(8,href.length);
                selectByValue(formGeneralObj, 'externalurlprefix', 'https://', true);
                setFormValue('externalurl', href, 0);
            } else if (href.indexOf('ftp://') == 0) {
                href = href.substr(6,href.length);
                selectByValue(formGeneralObj, 'externalurlprefix', 'ftp://', true);
                setFormValue('externalurl', href, 0);
            }
        } else {
            getCurrentFolderListing();
        }
    }
}

function getOption(opts, name) {
    return typeof(opts[name]) == "undefined" ? "" : opts[name];
}

function getPopupHref(href) {
    var formAdvancedObj = document.forms[3];
    var popuphref = "javascript:window.open('";

    popuphref += href + "','";
    popuphref += formAdvancedObj.popupname.value + "','";

    if (formAdvancedObj.popuplocation.checked)
        popuphref += "location=yes,";

    if (formAdvancedObj.popupscrollbars.checked)
        popuphref += "scrollbars=yes,";

    if (formAdvancedObj.popupmenubar.checked)
        popuphref += "menubar=yes,";

    if (formAdvancedObj.popupresizable.checked)
        popuphref += "resizable=yes,";

    if (formAdvancedObj.popuptoolbar.checked)
        popuphref += "toolbar=yes,";

    if (formAdvancedObj.popupstatus.checked)
        popuphref += "status=yes,";

    if (formAdvancedObj.popupdependent.checked)
        popuphref += "dependent=yes,";

    if (formAdvancedObj.popupwidth.value != "")
        popuphref += "width=" + formAdvancedObj.popupwidth.value + ",";

    if (formAdvancedObj.popupheight.value != "")
        popuphref += "height=" + formAdvancedObj.popupheight.value + ",";

    if (formAdvancedObj.popupleft.value != "") {
        if (formAdvancedObj.popupleft.value != "c")
            popuphref += "left=" + formAdvancedObj.popupleft.value + ",";
        else
            popuphref += "left='+(screen.availWidth/2-" + (formAdvancedObj.popupwidth.value/2) + ")+',";
    }

    if (formAdvancedObj.popuptop.value != "") {
        if (formAdvancedObj.popuptop.value != "c")
            popuphref += "top=" + formAdvancedObj.popuptop.value + ",";
        else
            popuphref += "top='+(screen.availHeight/2-" + (formAdvancedObj.popupheight.value/2) + ")+',";
    }

    if (popuphref.charAt(popuphref.length-1) == ',')
        popuphref = popuphref.substring(0, popuphref.length-1);

    popuphref += "');";

    if (formAdvancedObj.popupreturn.checked)
        popuphref += "return false;";

    return popuphref;
}

function setAttrib(elm, attrib, value, formnr) {
    var formObj = document.forms[formnr];
    var valueElm = formObj.elements[attrib.toLowerCase()];
    var dom = tinyMCEPopup.editor.dom;

    if (typeof(value) == "undefined" || value == null) {
        value = "";

        if (valueElm)
            value = valueElm.value;
    }

    dom.setAttrib(elm, attrib, value);
}

function getInputValue(name, formnr) {
    return document.forms[formnr].elements[name].value;
}

function getRadioValue(name, formnr) {
    var value = "";
    var elm = document.forms[formnr][name];
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

    return value;
}

function setRadioValue(name, value, formnr) {
    var elm = document.forms[formnr][name];
    if (elm && typeof(elm.value) == 'undefined') {
        for (var i = 0; i < elm.length; i++) {
            if (elm[i].value == value) {
                elm[i].checked = true;
            }
        }
    } else if (elm) {
        if (elm.value == value) {
            elm.checked = true;
        }
    }
}

function buildHref() {
    var href = "", name, title, i;
    var inst = tinyMCEPopup.editor;

    if (isVisible('external_panel')) {
        var externalurlprefix = document.getElementById('externalurlprefix');
        href = externalurlprefix.options[externalurlprefix.selectedIndex].value;

        if (document.getElementById('externalurl').value == "") {
            href = "";
        } else {
            href += document.getElementById('externalurl').value;
        }
    } else if (isVisible('anchors_panel')) {
        href = getRadioValue('anchorlink', 0);
        var url_match = href.match(/^#mce-new-anchor-(.*)$/);
        if (url_match != null) {
            nodes = inst.dom.select('h2,h3');
            for (i=0; i<nodes.length; i++) {
                title = nodes[i].innerHTML;
                name = title.toLowerCase();
                name = name.replace(/[^a-z]/g, '-');
                if (name == url_match[1]) {
                    nodes[i].innerHTML = '<a name="' + name + '" class="mceItemAnchor"></a>' + nodes[i].innerHTML;
                }
            }
            href = '#' + url_match[1];
        }
    } else if (isVisible('mail_panel')) {
        var mailaddress = getInputValue('mailaddress', 0);
        var mailsubject = getInputValue('mailsubject', 0);
        href = mailaddress;
        if (mailsubject != "") {
            href += "?subject=" + mailsubject;
        }
        if (href != "") {
            href = "mailto:" + href;
        }
    } else {
        var internallink = getRadioValue('internallink', 0);
        href = internallink;
        var pageanchor = getSelectValue(document.forms[0], 'pageanchor');
        if (pageanchor != "") {
            href += '#' + pageanchor;
        }
    }

    document.forms[0].href.value = href;
}

function insertAction() {
    var inst = tinyMCEPopup.editor;
    var elm, elementArray, i;

    buildHref();
    elm = inst.selection.getNode();
    elm = inst.dom.getParent(elm, "A");

    // Remove element if there is no href
    if (!document.forms[0].href.value) {
        tinyMCEPopup.execCommand("mceBeginUndoLevel");
        i = inst.selection.getBookmark();
        inst.dom.remove(elm, 1);
        inst.selection.moveToBookmark(i);
        tinyMCEPopup.execCommand("mceEndUndoLevel");
        tinyMCEPopup.close();
        return;
    }

    tinyMCEPopup.execCommand("mceBeginUndoLevel");

    // Create new anchor elements
    if (elm == null) {
        inst.getDoc().execCommand("unlink", false, null);
        tinyMCEPopup.execCommand("CreateLink", false, "#mce_temp_url#", {skip_undo : 1});

        elementArray = tinymce.grep(inst.dom.select("a"), function(n) {return inst.dom.getAttrib(n, 'href') == '#mce_temp_url#';});
        for (i=0; i<elementArray.length; i++)
            setAllAttribs(elm = elementArray[i]);
    } else
        setAllAttribs(elm);

    // Don't move caret if selection was image
    if (elm && (elm.childNodes.length != 1 || elm.firstChild.nodeName != 'IMG')) {
        inst.focus();
        inst.selection.select(elm);
        inst.selection.collapse(0);
        tinyMCEPopup.storeSelection();
    }

    tinyMCEPopup.execCommand("mceEndUndoLevel");
    tinyMCEPopup.close();
}

function setAllAttribs(elm) {
    var formGeneralObj = document.forms[0];
    var formUploadObj = document.forms[1];
    var formAdvancedObj = document.forms[2];
    var formButtonsObj = document.forms[3];

    var href = formGeneralObj.href.value;
    var target = getSelectValue(formAdvancedObj, 'targetlist');

    if (target == 'popup') {
        setAttrib(elm, 'href', getPopupHref(href), 0);
    } else {
        setAttrib(elm, 'href', href, 0);
    }
    setAttrib(elm, 'title', formAdvancedObj.title.value, 2);
    if (target != 'popup') {
        setAttrib(elm, 'target', target, 2);
    }

    var dom = tinyMCEPopup.editor.dom;
    dom.removeClass(elm, 'internal-link');
    dom.removeClass(elm, 'external-link');
    dom.removeClass(elm, 'anchor-link');
    dom.removeClass(elm, 'mail-link');

    if (isVisible('external_panel')) {
        dom.addClass(elm, 'external-link');
    } else if (isVisible('anchors_panel')) {
        dom.addClass(elm, 'anchor-link');
    } else if (isVisible('mail_panel')) {
        dom.addClass(elm, 'mail-link');
    } else {
        dom.addClass(elm, 'internal-link');
    }
}

function setDetails(path, pageanchor) {
    // Sends a low level Ajax request
    tinymce.util.XHR.send({
        url : path + '/tinymce-jsondetails',
        type : 'POST',
        success : function(text) {
            var html = "";
            var data = eval('(' + text + ')');
            document.getElementById ('internal_details_title').innerHTML = data.title;
            
            if (data.thumb == "") {
                document.getElementById ('internal_details_description').innerHTML = data.description;
            } else {
                document.getElementById ('internal_details_description').innerHTML = '<img src="' + data.thumb + '" border="0" />';
            }
            
            if (data.anchors.length == 0) {
                document.getElementById ('pageanchorcontainer').style.display = 'none';
                document.getElementById ('pageanchorlabel').style.display = 'none';
                html = '<select id="pageanchor" name="pageanchor">';
                html += '<option value="">top of page (default)</option>';
                html += '</select>';
                document.getElementById ('pageanchorcontainer').innerHTML = html;
            } else {
                document.getElementById ('pageanchorcontainer').style.display = 'block';
                document.getElementById ('pageanchorlabel').style.display = 'block';
                html = '<select id="pageanchor" name="pageanchor">';
                html += '<option value="">top of page (default)</option>';
                for (var i = 0; i < data.anchors.length; i++) {
                    html += '<option value="' + data.anchors[i] + '">' + data.anchors[i] + '</option>';
                }
                html += '</select>';
            }
            document.getElementById ('pageanchorcontainer').innerHTML = html;
            if (pageanchor != '') {
                selectByValue(document.forms[0], 'pageanchor', pageanchor, true);
            }
            current_path = path;
            current_pageanchor = pageanchor;
            document.getElementById('internal_details_panel').style.display = 'block';
            document.getElementById('upload_panel').style.display = 'none';
        }
    });
}

function getFolderListing(path, method) {
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
                    html += '<div class="' + (i % 2 == 0 ? 'even' : 'odd');
                    html += '"><input onclick="setDetails(\'';
                    html += data.items[i].url + '\', \'\');" type="radio" class="noborder" name="internallink" value="';
                    if (tinyMCEPopup.editor.settings.link_using_uids) {
                        html += "resolveuid/" + data.items[i].uid;
                    } else {
                        html += data.items[i].url;
                    }
                    html += '"/> ';
                    if (data.items[i].icon.length) {
                        html += '<img src="' + data.items[i].icon + '" border="0"/> ';
                    }
                    if (data.items[i].is_folderish) {
                        html += '<a class="contenttype-' + data.items[i].normalized_type + '" ';
                        html += 'href="javascript:getFolderListing(\'' + data.items[i].url + '\',\'tinymce-jsonlinkablefolderlisting' + '\')">';
                        html += data.items[i].title;
                        html += '</a>';
                    } else {
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
                document.getElementById ('uponelevel').href = 'javascript:getFolderListing(\'' + data.parent_url + '\',\'tinymce-jsonlinkablefolderlisting' + '\')';
            }

            html = "";
            for (var i = 0; i < data.path.length; i++) {
                if (i != 0) {
                    html += " &rarr; ";
                }
                if (i == data.path.length - 1) {
                    html += data.path[i].title;
                } else {
                    html += '<a href="javascript:getFolderListing(\'' + data.path[i].url + '\',\'tinymce-jsonlinkablefolderlisting' + '\')">';
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
            current_path = path;
            document.forms[1].action = current_path + '/tinymce-upload';
            setRadioValue('internallink', current_link, 0);
            if (current_link != "") {
                if (current_link.indexOf('resolveuid') != -1) {
                    current_uid = current_link.split('resolveuid/')[1];
                    tinymce.util.XHR.send({
                        url : tinyMCEPopup.editor.settings.portal_url + '/portal_tinymce/tinymce-getpathbyuid?uid=' + current_uid,
                        type : 'GET',
                        success : function(text) {
                            current_url = getAbsoluteUrl(tinyMCEPopup.editor.settings.document_base_url, text);
                            setDetails(current_url, current_pageanchor);
                        }
                    });
                } else {
                    setDetails(current_link, current_pageanchor);
                }
            }
        }
    });
}
