var InitializedTinyMCEInstances = {};

function TinyMCEConfig(id) {
    this.id = id;
    this.widget_config = eval('(' + document.getElementById (this.id).title + ')');
    this.toolbars = [];

    this.init = function() {

        // Check if already initialized
        if (typeof (InitializedTinyMCEInstances[this.id]) != 'undefined') {
            return;
        }
        InitializedTinyMCEInstances[this.id] = 1;

        this.initToolbars();
        var format = document.getElementById(this.id + '_text_format');
        if (format && format.tagName.toLowerCase() == 'input' && format.value.indexOf('html') == -1) {
            return;
        }

        // Set textformat to html and hide selector
        var node = tinymce.DOM.get(this.id);
        node = tinymce.DOM.getParent(node, '.ArchetypesRichWidget,.richTextWidget');
        if (node != null) {
            node = tinymce.DOM.select('div.fieldTextFormat', node);
            if (node.length > 0) {
                tinymce.DOM.select('select', node[0])[0].value = 'text/html';
                tinymce.DOM.setStyle(node[0], 'display', 'none');
            }
        }

        for (var i = 0; i < this.widget_config.customplugins.length; i++) {
            if (this.widget_config.customplugins[i].indexOf('|') != -1) {
                e = this.widget_config.customplugins[i].split('|');
                tinymce.PluginManager.load(e[0], this.getPortalUrl() + e[1]);
            }
        }
        var init_dict = {
            mode : "exact",
            elements : this.id,
            strict_loading_mode : true,
            theme : "advanced",
            language : this.getLanguage(),
            skin : "plone",
            inlinepopups_skin : "plonepopup",
            plugins : this.getPlugins(),
            // Remove images in data URIs
            setup : function(ed) {
               ed.onSaveContent.add(function(ed, o) {
                   // find all img's with src=data:image
                   var pattern=/\<img[^>]*src=[^>]*data:image[^>]*\>/g;
                   var filtered=o.content.replace(pattern, '');
                   o.content=filtered;
               });
            },
            // Find out if ieSpell requires gecko spellchecker...
            gecko_spellcheck : this.geckoSpellcheckEnabled(),

            atd_rpc_id : this.widget_config.atd_rpc_id,
            atd_rpc_url : this.widget_config.atd_rpc_url,
            atd_show_types : this.widget_config.atd_show_types,
            atd_ignore_strings : this.widget_config.atd_ignore_strings,

            labels : this.widget_config.labels,
            theme_advanced_styles : this.getStyles(),
            theme_advanced_buttons1 : this.getToolbar(0),
            theme_advanced_buttons2 : this.getToolbar(1),
            theme_advanced_buttons3 : this.getToolbar(2),
            theme_advanced_buttons4 : this.getToolbar(3),
            theme_advanced_toolbar_location : this.getToolbarLocation(),
            theme_advanced_toolbar_align : "left",
            theme_advanced_path_location : this.getPathLocation(),
            theme_advanced_path : false,
            theme_advanced_resizing : this.getResizing(),
            theme_advanced_resizing_use_cookie : this.getResizingUseCookie(),
            theme_advanced_resize_horizontal : this.getResizeHorizontal(),
            theme_advanced_source_editor_width : this.getEditorWidth(),
            theme_advanced_source_editor_height : this.getEditorHeight(),

            table_styles : this.getTableStyles(),
            table_firstline_th : true,
            directionality : this.getDirectionality(),
            entity_encoding : this.getEntityEncoding(),
            content_css : this.getContentCSS(),
            body_class : "documentContent",
            body_id : "content",
            document_base_url : this.getBase(),
            document_url : this.getDocumentUrl(),
            portal_url : this.getPortalUrl(),
            navigation_root_url : this.getNavigationRootUrl(),
            livesearch : this.getLivesearch(),
            valid_elements : this.getValidElements(),
            valid_inline_styles : this.getValidInlineStyles(),
            link_using_uids : this.getLinkUsingUids(),
            allow_captioned_images : this.getAllowCaptionedImages(),
            rooted : this.getRooted(),
            force_span_wrappers : true,
            fix_list_elements : false,
            // allow embed tag if user removes it from
            // list of nasty tags - see #10681
            media_strict: false
        };

        window.tinyMCE.init(init_dict);
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
        h['Lists'].push('{ title: "Lists", tag: "dl", className: "-", type: "Lists" }');
        h['Print'].push('{ title: "Print", tag: "", className: "-", type: "Print" }');

        // Add defaults
        h['Text'].push('{ title: "' + this.widget_config.labels['label_paragraph'] + '", tag: "p", className: "", type: "Text" }');
        h['Selection'].push('{ title: "' + this.widget_config.labels['label_styles'] + '", tag: "", className: "", type: "Selection" }');
        h['Tables'].push('{ title: "'+this.widget_config.labels['label_plain_cell'] +'", tag: "td", className: "", type: "Tables" }');
        h['Lists'].push('{ title: "'+this.widget_config.labels['label_lists'] +'", tag: "dl", className: "", type: "Lists" }');

        for (var i = 0; i < this.widget_config.styles.length; i++) {
            e = this.widget_config.styles[i].split('|');
            if (e.length <= 2) {
                e[2] = "";
            }
            switch (e[1].toLowerCase()) {
                case 'del':
                case 'ins':
                case 'span':
                    styletype = "Selection";
                    break;
                case 'tr':
                case 'td':
                case 'th':
                case 'table':
                    styletype = "Tables";
                    break;
                case 'ul':
                case 'ol':
                case 'li':
                case 'dt':
                case 'dd':
                case 'dl':
                    styletype = "Lists";
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

    this.getValidInlineStyles = function() {
        return this.widget_config.valid_inline_styles.join (',');
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
        return this.widget_config.document_url;
    };

    this.getBase = function() {
        return this.widget_config.parent;
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

    this.getDirectionality = function () {
        return this.widget_config.directionality;
    };

    this.getEntityEncoding = function () {
        return this.widget_config.entity_encoding;
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

    this.getAllowCaptionedImages = function () {
        return this.widget_config.allow_captioned_images;
    };

    this.getRooted = function () {
        return this.widget_config.rooted;
    };

    this.getPortalUrl = function () {
        return this.widget_config.portal_url;
    };

    this.getNavigationRootUrl = function () {
        return this.widget_config.navigation_root_url;
    };

    this.getLivesearch = function () {
        return this.widget_config.livesearch;
    };

    this.getSpellchecker = function () {
        var sp = this.widget_config.libraries_spellchecker_choice;
        if ((sp != '') && (sp != 'browser')) {
            return sp;
        }
        else {
            return;
        }
    };

    this.geckoSpellcheckEnabled = function () {
        if (this.widget_config.libraries_spellchecker_choice == 'browser') {
            return true;
        }
        else {
            return false;
        }
    };

    this.getPlugins = function () {
        var plugins = "safari,pagebreak,table,save,advhr,emotions,insertdatetime,preview,media,searchreplace,print,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,inlinepopups,plonestyle,tabfocus,definitionlist,ploneinlinestyles";

        var sp = this.getSpellchecker();
        if (sp) {
            plugins += ',' + sp;
        }

        for (var i = 0; i < this.widget_config.customplugins.length; i++) {
            if (this.widget_config.customplugins[i].indexOf('|') == -1) {
                plugins += ',' + this.widget_config.customplugins[i];
            } else {
                plugins += ',' + this.widget_config.customplugins[i].split('|')[0];
            }
        }
        if (this.widget_config.contextmenu) {
            plugins += ',contextmenu';
        }
        if (this.widget_config.autoresize) {
            plugins += ',autoresize';
        }
        return plugins;
    };
}

if (typeof(kukit) != "undefined") {
    kukit.actionsGlobalRegistry.register("init-tinymce", function(oper) {
        var config = new TinyMCEConfig(oper.node.id);
        delete InitializedTinyMCEInstances[oper.node.id];
        config.init();
    });

    kukit.actionsGlobalRegistry.register("save-tinymce", function(oper) {
        if(tinymce.EditorManager != undefined && tinymce.EditorManager.activeEditor != null){
            tinymce.EditorManager.activeEditor.save();
        }
    });
}
