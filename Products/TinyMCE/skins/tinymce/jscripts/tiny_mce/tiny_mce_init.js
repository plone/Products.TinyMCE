function TinyMCEConfig(id) {
	this.id = id;
	this.widget_config = eval('(' + document.getElementById (this.id).title + ')');
	this.toolbars = [];

	this.init = function() {
		this.initToolbars();
	};

	this.getButtonWidth = function(b) {
		switch (b) {
			case 'style':
				return 150;
			case 'forecolor':
				return 32;
			case 'backcolor':
				return 32;
			case 'tablecontrols':
				return 285;
		}
		return 23;
	};

	this.getTableStyles = function() {
		return this.widget_config.table_styles.join (";");
	};

	this.getToolbar = function(i) {
		return this.toolbars[i];
	};

	this.initToolbars = function() {
		var t = [[],[],[],[]];
		var cur_toolbar = 0;
		var cur_x = 0;
		var button_width;

		for (var i = 0; i < this.widget_config.buttons.length; i++) {
			button_width = this.getButtonWidth(this.widget_config.buttons[i]);
			if (cur_x + button_width > this.widget_config.toolbar_width) {
				cur_x = button_width;
				cur_toolbar++;
			} else {
				cur_x += button_width;
			}
			if (cur_toolbar <= 3) {
				t[cur_toolbar].push (this.widget_config.buttons[i]);
			}
		}

		this.toolbars = [t[0].join(','), t[1].join(','), t[2].join(','), t[3].join(',')];
	};

	this.getStyles = function() {
		var h = {'Text': [], 'Selection': [], 'Tables': [], 'Lists': [], 'Print': []};
		var styletype = "";

		// Push title
		h['Text'].push('{ title: "Text", tag: "", className: "-", type: "Text" }');
		h['Selection'].push('{ title: "Selection", tag: "", className: "-", type: "Selection" }');
		h['Tables'].push('{ title: "Tables", tag: "table", className: "-", type: "Tables" }');
		h['Lists'].push('{ title: "Lists", tag: "ul", className: "-", type: "Lists" }');
		h['Lists'].push('{ title: "Lists", tag: "ol", className: "-", type: "Lists" }');
		h['Print'].push('{ title: "Print", tag: "", className: "-", type: "Print" }');

		// Add defaults
		h['Text'].push('{ title: "Normal paragraph", tag: "p", className: "", type: "Text" }');

		h['Lists'].push('{ title: "Disc", tag: "ul", className: "", listType: "disc", type: "Lists" }');
		h['Lists'].push('{ title: "Square", tag: "ul", className: "", listType: "square", type: "Lists" }');
		h['Lists'].push('{ title: "Circle", tag: "ul", className: "", listType: "circle", type: "Lists" }');

		h['Lists'].push('{ title: "Numbers", tag: "ol", className: "", listType: "1", type: "Lists" }');
		h['Lists'].push('{ title: "Lower Alpha", tag: "ol", className: "", listType: "a", type: "Lists" }');
		h['Lists'].push('{ title: "Upper Alpha", tag: "ol", className: "", listType: "A", type: "Lists" }');
		h['Lists'].push('{ title: "Lower Roman", tag: "ol", className: "", listType: "i", type: "Lists" }');
		h['Lists'].push('{ title: "Upper Roman", tag: "ol", className: "", listType: "I", type: "Lists" }');

		for (var i = 0; i < this.widget_config.styles.length; i++) {
			e = this.widget_config.styles[i].split('|');
			if (e.length <= 2) {
				e[2] = "";
			}
			switch (e[1].toLowerCase()) {
				case 'span':
					styletype = "Selection";
					break;
				case 'tr':
				case 'td':
				case 'th':
				case 'table':
					styletype = "Tables";
					break;
				default:
					styletype = "Text";
					break;
			}
			if (e[2] == "pageBreak") {
				styletype = "Print";
			}
			h[styletype].push('{ title: "' + e[0] + '", tag: "' + e[1] + '", className: "' + e[2] + '", type: "' + styletype + '" }');
		}
		h['Selection'].push('{ title: "(remove style)", tag: "", className: "", type: "Selection" }');
		h['Tables'].push('{ title: "Plain cell", tag: "td", className: "", type: "Tables" }');

		// Add items to array
		var a = [];
		if (h['Text'].length > 1) {
			for (var i = 0; i < h['Text'].length; i++) {
				a.push(h['Text'][i]);
			}
		}
		if (h['Selection'].length > 1) {
			for (var i = 0; i < h['Selection'].length; i++) {
				a.push(h['Selection'][i]);
			}
		}
		if (h['Tables'].length > 1) {
			for (var i = 0; i < h['Tables'].length; i++) {
				a.push(h['Tables'][i]);
			}
		}
		if (h['Lists'].length > 1) {
			for (var i = 0; i < h['Lists'].length; i++) {
				a.push(h['Lists'][i]);
			}
		}
		if (h['Print'].length > 1) {
			for (var i = 0; i < h['Print'].length; i++) {
				a.push(h['Print'][i]);
			}
		}
		return '[' + a.join(',') + ']';
	};

	this.getValidElements = function() {
		a = [];

		for (var valid_element in this.widget_config.valid_elements) {
			var s = valid_element;
			if (this.widget_config.valid_elements[valid_element].length > 0) {
				s += '[' + this.widget_config.valid_elements[valid_element].join ('|') + ']';
			}
			a.push (s);
		}
		return a.join (',');
	};

	this.getDocumentUrl = function() {
		var href_string = document.location.href;
		var href_array = href_string.split('/');
		if (href_string.indexOf('portal_factory') != -1) {
			while (href_array[href_array.length-1] != 'portal_factory') {
				href_array.pop();
			}
			href_array.pop();
		} else {
			if (href_array.length > 4) {
				href_array.pop();
			}
		}
		return href_array.join('/');
	};

	this.getBase = function() {
		var href_string = document.location.href;
		var href_array = href_string.split('/');
		if (href_string.indexOf('portal_factory') != -1) {
			while (href_array[href_array.length-1] != 'portal_factory') {
				href_array.pop();
			}
			href_array.pop();
		} else {
			if (href_array.length > 4) {
				href_array.pop();
			}
			if (href_array.length > 4) {
				href_array.pop();
			}
		}
		return href_array.join('/') + '/';
	};

	this.getToolbarLocation = function () {
		return this.widget_config.toolbar_location;
	};

	this.getPathLocation = function () {
		return this.widget_config.path_location;
	};

	this.getResizing = function () {
		return this.widget_config.resizing;
	};

	this.getResizingUseCookie = function () {
		return this.widget_config.resizing_use_cookie;
	};

	this.getResizeHorizontal = function () {
		return this.widget_config.resize_horizontal;
	};

	this.getEditorWidth = function () {
		return this.widget_config.editor_width;
	};

	this.getEditorHeight = function () {
		return this.widget_config.editor_height;
	};

	this.getAutoresize = function () {
		return this.widget_config.autoresize;
	};

	this.getDirectionality = function () {
		return this.widget_config.directionality;
	};

	this.getContentCSS = function () {
		return this.widget_config.content_css;
	};

	this.getLanguage = function () {
		return this.widget_config.language;
	};

	this.getLinkUsingUids = function () {
		return this.widget_config.link_using_uids;
	};

	this.getPortalUrl = function () {
		return this.widget_config.portal_url;
	};
}

kukit.actionsGlobalRegistry.register("init-tinymce", function(oper) {
	var config = new TinyMCEConfig(oper.node.id);
	config.init();

	window.tinyMCE.init({
		mode : "exact",
		elements : oper.node.id,
		strict_loading_mode : true,
		theme : "advanced",
		language : config.getLanguage(),
		skin : "plone",
		inlinepopups_skin : "plonepopup",
		plugins : "safari,pagebreak,table,save,advhr,advimage,advlink,emotions,iespell,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,inlinepopups,style",

		theme_advanced_styles : config.getStyles(),
		theme_advanced_buttons1 : config.getToolbar(0),
		theme_advanced_buttons2 : config.getToolbar(1),
		theme_advanced_buttons3 : config.getToolbar(2),
		theme_advanced_buttons4 : config.getToolbar(3),
		theme_advanced_toolbar_location : config.getToolbarLocation(),
		theme_advanced_toolbar_align : "left",
		theme_advanced_path_location : config.getPathLocation(),
		theme_advanced_path : false,
		theme_advanced_resizing : config.getResizing(),
		theme_advanced_resizing_use_cookie : config.getResizingUseCookie(),
		theme_advanced_resize_horizontal : config.getResizeHorizontal(),
		theme_advanced_source_editor_width : config.getEditorWidth(),
		theme_advanced_source_editor_height : config.getEditorHeight(),
  
		auto_resize : config.getAutoresize(),
		table_styles : config.getTableStyles(),
		directionality : config.getDirectionality(),
		content_css : config.getContentCSS(),
		body_class : "documentContent",
		document_base_url : config.getBase(),
		document_url : config.getDocumentUrl(),
		portal_url : config.getPortalUrl(),
		valid_elements : config.getValidElements(),
		link_using_uids : config.getLinkUsingUids()
	});
});

kukit.actionsGlobalRegistry.register("save-tinymce", function(oper) {
	tinymce.EditorManager.activeEditor.save();
});
