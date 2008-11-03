var ImageDialog = {
	current_path : "",
	current_link : "",
	
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

		tinyMCEPopup.resizeToInnerSize();

		if (n.nodeName == 'IMG') {
			var href = dom.getAttrib(n, 'src');
			if (href.indexOf('/')) {
				var href_array = href.split('/');
				var last = href_array[href_array.length-1];
				if ((last == 'image_large') ||
					(last == 'image_preview') ||
					(last == 'image_mini') ||
					(last == 'image_thumb') ||
					(last == 'image_tile') ||
					(last == 'image_icon') ||
					(last == 'image_listing')) {
					var dimensions = href_array.pop();
					selectByValue(f0, 'dimensions', dimensions, true);
					href = href_array.join ('/');
				}
			}
			var alt = dom.getAttrib(n, 'alt');
			var classnames = dom.getAttrib(n, 'class').split(' ');
			var classname = "";
			for (var i = 0; i < classnames.length; i++) {
				if (classnames[i] == 'captioned') {
					f0.caption.checked = true;
				} else {
					classname = classnames[i];
				}
			}
			nl0.alt.value = alt;
			selectByValue(f0, 'classes', classname, true);
			nl2.insert.value = ed.getLang('update');

			href = this.getAbsoluteUrl(tinyMCEPopup.editor.settings.document_base_url, href);
			this.current_link = href;
			this.getFolderListing(this.getParentUrl(href));
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
			alt : nl0.alt.value,
			'class' : this.getSelectValue(f0, 'classes') + (f0.elements['caption'].checked ? ' captioned' : '')
		};

		el = ed.selection.getNode();

		if (el && el.nodeName == 'IMG') {
			ed.dom.setAttribs(el, args);
		} else {
			ed.execCommand('mceInsertContent', false, '<img id="__mce_tmp" />', {skip_undo : 1});
			ed.dom.setAttribs('__mce_tmp', args);
			ed.dom.setAttrib('__mce_tmp', 'id', '');
			ed.undoManager.add();
		}

		tinyMCEPopup.close();
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

	resetImageData : function() {
		var f = document.forms[0];

		f.elements.width.value = f.elements.height.value = '';
	},

	updateImageData : function(img, st) {
		var f = document.forms[0];

		if (!st) {
			f.elements.width.value = img.width;
			f.elements.height.value = img.height;
		}

		this.preloadImg = img;
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

	updateStyle : function(ty) {
		var dom = tinyMCEPopup.dom, st, v, f = document.forms[0], img = dom.create('img', {style : dom.get('style').value});

		if (tinyMCEPopup.editor.settings.inline_styles) {
			// Handle align
			if (ty == 'align') {
				dom.setStyle(img, 'float', '');
				dom.setStyle(img, 'vertical-align', '');

				v = this.getSelectValue(f, 'align');
				if (v) {
					if (v == 'left' || v == 'right')
						dom.setStyle(img, 'float', v);
					else
						img.style.verticalAlign = v;
				}
			}

			// Handle border
			if (ty == 'border') {
				dom.setStyle(img, 'border', '');

				v = f.border.value;
				if (v || v == '0') {
					if (v == '0')
						img.style.border = '0';
					else
						img.style.border = v + 'px solid black';
				}
			}

			// Handle hspace
			if (ty == 'hspace') {
				dom.setStyle(img, 'marginLeft', '');
				dom.setStyle(img, 'marginRight', '');

				v = f.hspace.value;
				if (v) {
					img.style.marginLeft = v + 'px';
					img.style.marginRight = v + 'px';
				}
			}

			// Handle vspace
			if (ty == 'vspace') {
				dom.setStyle(img, 'marginTop', '');
				dom.setStyle(img, 'marginBottom', '');

				v = f.vspace.value;
				if (v) {
					img.style.marginTop = v + 'px';
					img.style.marginBottom = v + 'px';
				}
			}

			// Merge
			dom.get('style').value = dom.serializeStyle(dom.parseStyle(img.style.cssText));
		}
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

	setDetails : function(path) {
		// Sends a low level Ajax request
		tinymce.util.XHR.send({
		    url : path + '/tinymce-jsondetails',
			type : 'POST',
			success : function(text) {
				var html = "";
				var data = eval('(' + text + ')');
			
				if (data.thumb == "") {
					document.getElementById ('previewimagecontainer').innerHTML = data.description;
				} else {
					document.getElementById ('previewimagecontainer').innerHTML = '<img src="' + data.thumb + '" border="0" />';
				}
	
				this.current_path = path;
			}
		});	
	},

	getCurrentFolderListing : function() {
		this.getFolderListing(this.getParentUrl(tinyMCEPopup.editor.settings.document_base_url));
	},
	
	getFolderListing : function(path) {
		// Sends a low level Ajax request
		tinymce.util.XHR.send({
		    url : path + '/tinymce-jsonimagefolderlisting',
			type : 'POST',
			success : function(text) {
				var html = "";
				var data = eval('(' + text + ')');
				if (data.items.length == 0) {
					html = "No items in this folder";
				} else {
					for (var i = 0; i < data.items.length; i++) {
						html += '<div class="' + (i % 2 == 0 ? 'even' : 'odd') + '">';
						if (data.items[i].is_folderish) {
							html += '<img src="' + data.items[i].icon + '" border="0" style="margin-left: 17px" /> ';
							html += '<a href="javascript:ImageDialog.getFolderListing(\'' + data.items[i].url + '\')">';
							html += data.items[i].title;
							html += '</a>';
						} else {
							html += '<input onclick="ImageDialog.setDetails(\'' + data.items[i].url + '\');" type="radio" class="noborder" name="internallink" value="' + data.items[i].url + '"/> <img src="' + data.items[i].icon + '" border="0"/> ';
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
					document.getElementById ('uponelevel').href = 'javascript:ImageDialog.getFolderListing(\'' + data.parent_url + '\')';
				}

				html = "";
				for (var i = 0; i < data.path.length; i++) {
					if (i != 0) {
						html += " - ";
					}
					if (i == data.path.length - 1) {
						html += data.path[i].title;
					} else {
						html += '<a href="javascript:ImageDialog.getFolderListing(\'' + data.path[i].url + '\')">';
						html += data.path[i].title;
						html += '</a>';
					}
				}
				document.getElementById ('internalpath').innerHTML = html;
	
				// Set global path
				ImageDialog.current_path = path;
				document.forms[1].action = ImageDialog.current_path + '/tinymce-upload';
				ImageDialog.setRadioValue('internallink', ImageDialog.current_link, 0);
				if (ImageDialog.current_link != "") {
					ImageDialog.setDetails(ImageDialog.current_link);
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
	ImageDialog.displayPanel('internal_panel');
	ImageDialog.getFolderListing(ImageDialog.current_path);
}

function uploadError(error_msg) {
	alert (error_msg);
}

ImageDialog.preInit();
tinyMCEPopup.onInit.add(ImageDialog.init, ImageDialog);
