/* Functions for the advlink plugin popup */

tinyMCEPopup.requireLangPack();

var templates = {
	"window.open" : "window.open('${url}','${target}','${options}')"
};

var current_path;
var current_link = "";
var current_url = "";
var current_pageanchor = "";

function preinit() {
	var url;

	if (url = tinyMCEPopup.getParam("external_link_list_url"))
		document.write('<script language="javascript" type="text/javascript" src="' + tinyMCEPopup.editor.documentBaseURI.toAbsolute(url) + '"></script>');
}

function init() {
	tinyMCEPopup.resizeToInnerSize();

	var formGeneralObj = document.forms[0];
	var formUploadObj = document.forms[1];
	var formAdvancedObj = document.forms[2];
	var formButtonsObj = document.forms[3];
	var inst = tinyMCEPopup.editor;
	var elm = inst.selection.getNode();
	var action = "insert";
	var html;

	document.getElementById('anchorlinkcontainer').innerHTML = getAnchorListHTML();

	// Check if update or insert
	elm = inst.dom.getParent(elm, "A");
	if (elm != null && elm.nodeName == "A")
		action = "update";

	// Set button caption
	formButtonsObj.insert.value = tinyMCEPopup.getLang(action, 'Insert', true); 

	if (action == "update") {
		var href = inst.dom.getAttrib(elm, 'href');

		// Setup form data
		setFormValue('href', href, 0);
		if ((typeof(elm.title) != "undefined") && (elm.title != "")) {
			setFormValue('title', inst.dom.getAttrib(elm, 'title'), 2);
		}

		// Check if anchor
		if (href.charAt(0) == '#') {
			displayPanel('anchors_panel');
			setRadioValue('anchorlink', href, 0);
		} else if (href.indexOf('mailto:') != -1) {
			displayPanel('mail_panel');
			var mailaddress = href.split('mailto:')[1];
			var mailsubject = "";
			
			if (mailaddress.indexOf('?subject=') != -1) {
				mailsubject = mailaddress.split('?subject=')[1];
				mailaddress = mailaddress.split('?subject=')[0];
			}
			
			setFormValue('mailaddress', mailaddress, 0);
			setFormValue('mailsubject', mailsubject, 0);
		} else if ((href.indexOf('http://') != -1) || (href.indexOf('https://') != -1) || (href.indexOf('ftp://') != -1)) {
			displayPanel('external_panel');
			if (href.indexOf('http://') != -1) {
				selectByValue(formGeneralObj, 'externalurlprefix', 'http://', true);
				setFormValue('externalurl', href.split('http://')[1], 0);
			} else if (href.indexOf('https://') != -1) {
				selectByValue(formGeneralObj, 'externalurlprefix', 'https://', true);
				setFormValue('externalurl', href.split('https://')[1], 0);
			} else if (href.indexOf('ftp://') != -1) {
				selectByValue(formGeneralObj, 'externalurlprefix', 'ftp://', true);
				setFormValue('externalurl', href.split('ftp://')[1], 0);
			}
		} else {
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
        if ((href.indexOf('http://') != -1) || (href.indexOf('https://') != -1) || (href.indexOf('ftp://') != -1)) {
            displayPanel('external_panel');
            if (href.indexOf('http://') != -1) {
                selectByValue(formGeneralObj, 'externalurlprefix', 'http://', true);
                setFormValue('externalurl', href.split('http://')[1], 0);
            } else if (href.indexOf('https://') != -1) {
                selectByValue(formGeneralObj, 'externalurlprefix', 'https://', true);
                setFormValue('externalurl', href.split('https://')[1], 0);
            } else if (href.indexOf('ftp://') != -1) {
                selectByValue(formGeneralObj, 'externalurlprefix', 'ftp://', true);
                setFormValue('externalurl', href.split('ftp://')[1], 0);
            }
        } else {
            getCurrentFolderListing();
        }
    }
}

function checkSearch(e) {
    if (tinyMCEPopup.editor.settings.livesearch || e.keyCode == 13) {
        getFolderListing(tinyMCEPopup.editor.settings.portal_url, 'tinymce-jsonlinkablesearch');
    }
}

function checkExternalUrl() {
    var formGeneralObj = document.forms[0];
    href = document.getElementById('externalurl').value;
    if ((href.indexOf('http://') != -1) || (href.indexOf('https://') != -1) || (href.indexOf('ftp://') != -1)) {
        if (href.indexOf('http://') != -1) {
            selectByValue(formGeneralObj, 'externalurlprefix', 'http://', true);
            setFormValue('externalurl', href.split('http://')[1], 0);
        } else if (href.indexOf('https://') != -1) {
            selectByValue(formGeneralObj, 'externalurlprefix', 'https://', true);
            setFormValue('externalurl', href.split('https://')[1], 0);
        } else if (href.indexOf('ftp://') != -1) {
            selectByValue(formGeneralObj, 'externalurlprefix', 'ftp://', true);
            setFormValue('externalurl', href.split('ftp://')[1], 0);
        }
    }
}
function getParentUrl(url) {
	var url_array = url.split('/');
	url_array.pop();
	return url_array.join('/');
}

function getAbsoluteUrl(base, link) {
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
}

function setFormValue(name, value, formnr) {
	document.forms[formnr].elements[name].value = value;
}

function parseWindowOpen(onclick) {
	var formGeneralObj = document.forms[0];
	var formUploadObj = document.forms[1];
	var formAdvancedObj = document.forms[2];
	var formButtonsObj = document.forms[3];

	// Preprocess center code
	if (onclick.indexOf('return false;') != -1) {
		formAdvancedObj.popupreturn.checked = true;
		onclick = onclick.replace('return false;', '');
	} else
		formAdvancedObj.popupreturn.checked = false;

	var onClickData = parseLink(onclick);

	if (onClickData != null) {
		formAdvancedObj.ispopup.checked = true;

		var onClickWindowOptions = parseOptions(onClickData['options']);
		var url = onClickData['url'];

		formAdvancedObj.popupname.value = onClickData['target'];
		formAdvancedObj.popupwidth.value = getOption(onClickWindowOptions, 'width');
		formAdvancedObj.popupheight.value = getOption(onClickWindowOptions, 'height');

		formAdvancedObj.popupleft.value = getOption(onClickWindowOptions, 'left');
		formAdvancedObj.popuptop.value = getOption(onClickWindowOptions, 'top');

		if (formAdvancedObj.popupleft.value.indexOf('screen') != -1)
			formAdvancedObj.popupleft.value = "c";

		if (formAdvancedObj.popuptop.value.indexOf('screen') != -1)
			formAdvancedObj.popuptop.value = "c";

		formAdvancedObj.popuplocation.checked = getOption(onClickWindowOptions, 'location') == "yes";
		formAdvancedObj.popupscrollbars.checked = getOption(onClickWindowOptions, 'scrollbars') == "yes";
		formAdvancedObj.popupmenubar.checked = getOption(onClickWindowOptions, 'menubar') == "yes";
		formAdvancedObj.popupresizable.checked = getOption(onClickWindowOptions, 'resizable') == "yes";
		formAdvancedObj.popuptoolbar.checked = getOption(onClickWindowOptions, 'toolbar') == "yes";
		formAdvancedObj.popupstatus.checked = getOption(onClickWindowOptions, 'status') == "yes";
		formAdvancedObj.popupdependent.checked = getOption(onClickWindowOptions, 'dependent') == "yes";
	}
}

function parseFunction(onclick) {
	var onClickData = parseLink(onclick);

	// TODO: Add stuff here
}

function getOption(opts, name) {
	return typeof(opts[name]) == "undefined" ? "" : opts[name];
}

function parseLink(link) {
	link = link.replace(new RegExp('&#39;', 'g'), "'");

	var fnName = link.replace(new RegExp("\\s*([A-Za-z0-9\.]*)\\s*\\(.*", "gi"), "$1");

	// Is function name a template function
	var template = templates[fnName];
	if (template) {
		// Build regexp
		var variableNames = template.match(new RegExp("'?\\$\\{[A-Za-z0-9\.]*\\}'?", "gi"));
		var regExp = "\\s*[A-Za-z0-9\.]*\\s*\\(";
		var replaceStr = "";
		for (var i=0; i<variableNames.length; i++) {
			// Is string value
			if (variableNames[i].indexOf("'${") != -1)
				regExp += "'(.*)'";
			else // Number value
				regExp += "([0-9]*)";

			replaceStr += "$" + (i+1);

			// Cleanup variable name
			variableNames[i] = variableNames[i].replace(new RegExp("[^A-Za-z0-9]", "gi"), "");

			if (i != variableNames.length-1) {
				regExp += "\\s*,\\s*";
				replaceStr += "<delim>";
			} else
				regExp += ".*";
		}

		regExp += "\\);?";

		// Build variable array
		var variables = [];
		variables["_function"] = fnName;
		var variableValues = link.replace(new RegExp(regExp, "gi"), replaceStr).split('<delim>');
		for (var i=0; i<variableNames.length; i++)
			variables[variableNames[i]] = variableValues[i];

		return variables;
	}

	return null;
}

function parseOptions(opts) {
	if (opts == null || opts == "")
		return [];

	// Cleanup the options
	opts = opts.toLowerCase();
	opts = opts.replace(/;/g, ",");
	opts = opts.replace(/[^0-9a-z=,]/g, "");

	var optionChunks = opts.split(',');
	var options = [];

	for (var i=0; i<optionChunks.length; i++) {
		var parts = optionChunks[i].split('=');

		if (parts.length == 2)
			options[parts[0]] = parts[1];
	}

	return options;
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

function previewExternalLink() {
	var url = "";
	var externalurlprefix = document.getElementById('externalurlprefix');
	url = externalurlprefix.options[externalurlprefix.selectedIndex].value;
	
	if (document.getElementById('externalurl').value == "") {
		url = "";
	} else {
		url += document.getElementById('externalurl').value;
	}
	
	if (url == "") {
		document.getElementById('previewexternal').src = "about:blank";
	} else {
		document.getElementById('previewexternal').src = url;
	}
}

function getAnchorListHTML() {
	var inst = tinyMCEPopup.editor;
	var nodes = inst.dom.select('a.mceItemAnchor,img.mceItemAnchor'), name, title, i;
	var html = "";
	var divclass ="even";

	for (i=0; i<nodes.length; i++) {
		if ((name = inst.dom.getAttrib(nodes[i], "name")) != "") {
			html += '<div class="' + divclass + '"><input type="radio" class="noborder" name="anchorlink" value="#' + name + '"/> ' + name + '</div>';
			divclass = divclass == "even" ? "odd" : "even";
		}
	}

	nodes = inst.dom.select('h2,h3');
	if (nodes.length > 0) {
		for (i=0; i<nodes.length; i++) {
			title = nodes[i].innerHTML;
			title_match = title.match(/mceItemAnchor/);
			if (title_match == null) {
				name = title.toLowerCase();
				name = name.replace(/[^a-z]/g, '-');
				html += '<div class="' + divclass + '"><input type="radio" class="noborder" name="anchorlink" value="#mce-new-anchor-' + name + '"/> ' + title + '</div>';
				divclass = divclass == "even" ? "odd" : "even";
			}
		}
	}

	if (html == "") {
		html = '<div class="odd">No anchors on this page</div>';
	}

	return html;
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
	if ((target != '_self') && (target != 'popup')) {
		setAttrib(elm, 'target', target, 2);
	}

	// Refresh in old MSIE
	if (tinyMCE.isMSIE5)
		elm.outerHTML = elm.outerHTML;
}

function getSelectValue(form_obj, field_name) {
	var elm = form_obj.elements[field_name];

	if (!elm || elm.options == null || elm.selectedIndex == -1)
		return "";

	return elm.options[elm.selectedIndex].value;
}

function getLinkListHTML(elm_id, target_form_element, onchange_func) {
	if (typeof(tinyMCELinkList) == "undefined" || tinyMCELinkList.length == 0)
		return "";

	var html = "";

	html += '<select id="' + elm_id + '" name="' + elm_id + '"';
	html += ' class="mceLinkList" onfocus="tinyMCE.addSelectAccessibility(event, this, window);" onchange="this.form.' + target_form_element + '.value=';
	html += 'this.options[this.selectedIndex].value;';

	if (typeof(onchange_func) != "undefined")
		html += onchange_func + '(\'' + target_form_element + '\',this.options[this.selectedIndex].text,this.options[this.selectedIndex].value);';

	html += '"><option value="">---</option>';

	for (var i=0; i<tinyMCELinkList.length; i++)
		html += '<option value="' + tinyMCELinkList[i][1] + '">' + tinyMCELinkList[i][0] + '</option>';

	html += '</select>';

	return html;

	// tinyMCE.debug('-- image list start --', html, '-- image list end --');
}

function setUploadVisibility() {
	if ((isVisible('internal_panel')) && (isVisible('general_panel'))) {
		document.getElementById('upload').style.display = 'inline';
	} else {
		document.getElementById('upload').style.display = 'none';
	}
}

function setPopupVisibility() {
	var targetlist = document.getElementById('targetlist');	
	if (targetlist.options[targetlist.selectedIndex].value == 'popup') {
		document.getElementById('popup_panel').style.display = 'block';
	} else {
		document.getElementById('popup_panel').style.display = 'none';
	}
}

function getTargetListHTML(elm_id, target_form_element) {
	var targets = tinyMCEPopup.getParam('theme_advanced_link_targets', '').split(';');
	var html = '';

	html += '<select id="' + elm_id + '" name="' + elm_id + '" onf2ocus="tinyMCE.addSelectAccessibility(event, this, window);" onchange="this.form.' + target_form_element + '.value=';
	html += 'this.options[this.selectedIndex].value;">';
	html += '<option value="_self">' + tinyMCEPopup.getLang('advlink_dlg.target_same') + '</option>';
	html += '<option value="_blank">' + tinyMCEPopup.getLang('advlink_dlg.target_blank') + ' (_blank)</option>';
	html += '<option value="_parent">' + tinyMCEPopup.getLang('advlink_dlg.target_parent') + ' (_parent)</option>';
	html += '<option value="_top">' + tinyMCEPopup.getLang('advlink_dlg.target_top') + ' (_top)</option>';

	for (var i=0; i<targets.length; i++) {
		var key, value;

		if (targets[i] == "")
			continue;

		key = targets[i].split('=')[0];
		value = targets[i].split('=')[1];

		html += '<option value="' + key + '">' + value + ' (' + key + ')</option>';
	}

	html += '</select>';

	return html;
}

function displayPanel(elm_id) {
	document.getElementById ('internal_panel').style.display = elm_id == 'internal_panel' || elm_id == 'upload_panel' ? 'block' : 'none';
	document.getElementById ('internal_details_panel').style.display = elm_id == 'internal_panel' ? 'block' : 'none';
	document.getElementById ('external_panel').style.display = elm_id == 'external_panel' ? 'block' : 'none';
	document.getElementById ('mail_panel').style.display = elm_id == 'mail_panel' ? 'block' : 'none';
	document.getElementById ('anchors_panel').style.display = elm_id == 'anchors_panel' ? 'block' : 'none';
	document.getElementById ('upload_panel').style.display = elm_id == 'upload_panel' ? 'block' : 'none';

	setUploadVisibility();
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
		}
	});	
}

function getCurrentFolderListing() {
	getFolderListing(tinyMCEPopup.editor.settings.document_base_url, 'tinymce-jsonlinkablefolderlisting'); 
}

function getFolderListing(path, method) {
	// Sends a low level Ajax request
	tinymce.util.XHR.send({
		url : path + '/' + method,
		content_type : "application/x-www-form-urlencoded",
		type : 'POST',
		data : "searchtext=" + document.getElementById('searchtext').value,
		success : function(text) {
			var html = "";
			var data = eval('(' + text + ')');
			if (data.items.length == 0) {
				html = "No items in this folder";
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
					html += '"/> <img src="' + data.items[i].icon + '" border="0"/> ';
					if (data.items[i].is_folderish) {
						html += '<a href="javascript:getFolderListing(\'' + data.items[i].url + '\',\'tinymce-jsonlinkablefolderlisting' + '\')">';
						html += data.items[i].title;
						html += '</a>';
					} else {
						html += data.items[i].title;
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
					html += " - ";
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
	
			// Set global path
			current_path = path;
			document.forms[1].action = current_path + '/tinymce-upload';
			setRadioValue('internallink', current_link, 0);
			if (current_link != "") {
				if (current_link.indexOf('resolveuid') != -1) {
					setDetails(current_url, current_pageanchor);
				} else {
					setDetails(current_link, current_pageanchor);
				}
			}
		}
	});
}

function uploadOk(ok_msg) {
	current_link = ok_msg;
	displayPanel('internal_panel');
	getFolderListing(current_path + '\',\'tinymce-jsonlinkablefolderlisting');
}

function uploadError(error_msg) {
	alert (error_msg);
}

// While loading
preinit();
tinyMCEPopup.onInit.add(init);
