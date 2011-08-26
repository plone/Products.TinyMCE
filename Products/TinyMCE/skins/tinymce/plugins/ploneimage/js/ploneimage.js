/*jslint regexp: true,
         browser: true,
         sloppy: true,
         white: true,
         plusplus: true,
         indent: 4 */
/*global jq, tinymce, tinyMCEPopup */
/**
 * Image selection dialog.
 *
 * @param mcePopup Reference to a corresponding TinyMCE popup object.
 */
var ImageDialog = function (mcePopup) {
    var image_list_url;

    this.tinyMCEPopup = mcePopup;
    this.editor = mcePopup.editor;

    /* In case of UID linked images maintains a relative "resolveuid/<UUID>"
       fragment otherwise contains a full URL to the image. */
    this.current_link = "";

    /* Absolute base URL to an image (without scaling path components)
       regardless whether the image was referenced using an UID or a direct
       link. */
    this.current_url = "";

    /* List of additional CSS classes set on the <img/> element which have no
       special meaning for TinyMCE. These are passed through as is. */
    this.current_classes = [];
    this.is_search_activated = false;

    /* Translatable UI labels */
    this.labels = this.editor.getParam("labels");

    /* URL of the thumbnail image shown on the right side details pane when
       an image is selected.  */
    this.thumb_url = "";

    this.tinyMCEPopup.requireLangPack();

    // TODO: WTF?
    image_list_url = this.tinyMCEPopup.getParam("external_image_list_url");
    if (image_list_url) {
        jq.getScript(this.editor.documentBaseURI.toAbsolute(image_list_url));
    }
};


/**
 * Dialog initialization.
 *
 * This will be called when the dialog is activated by pressing the
 * corresponding toolbar icon.
 */
ImageDialog.prototype.init = function () {
    var self = this,
        selected_node = jq(this.editor.selection.getNode(), document),
        scaled_image,
        current_uid;

    this.tinyMCEPopup.resizeToInnerSize();

    jq('#action-form', document).submit(function (e) {
        e.preventDefault();
        self.insert();
    });
    jq('#upload', document).click(function (e) {
        e.preventDefault();
        self.displayUploadPanel();
    });
    jq('#cancel', document).click(function (e) {
        e.preventDefault();
        self.tinyMCEPopup.close();
    });
    jq('#searchtext', document).keyup(function (e) {
        e.preventDefault();
        // We need to stop the event from propagating so that pressing Esc will
        // only stop the search but not close the whole dialog.
        e.stopPropagation();
        self.checkSearch(e);
    });
    // handle different folder listing view types
    jq('#general_panel .legend a', document).click(function (e) {
        e.preventDefault();
        jq('#general_panel .legend a', document).removeClass('current');
        jq(this).addClass('current');
        // refresh listing with new view settings
        self.getFolderListing(self.folderlisting_context_url, self.folderlisting_method);
    });

    if (!this.editor.settings.allow_captioned_images) {
        jq('#caption', document).parent().parent().hide();
    }
    if (this.editor.settings.rooted) {
        jq('#home', document).hide();
    }

    if (selected_node.get(0).tagName && selected_node.get(0).tagName.toUpperCase() === 'IMG') {
        /** The image dialog was opened to edit an existing image element. **/

        // Manage the CSS classes defined in the <img/> element. We handle the
        // following classes as special cases:
        //   - captioned
        //   - image-inline
        //   - image-left
        //   - image-right
        // and pass all other classes through as-is.
        jq.each(selected_node.attr('class').split(/\s+/), function () {
            var classname = this.toString();
            switch (classname) {
                case 'captioned':
                    if (self.editor.settings.allow_captioned_images) {
                        // Check the caption checkbox
                        jq('#caption', document).attr('checked', 'checked');
                    }
                    break;

                case 'image-inline':
                case 'image-left':
                case 'image-right':
                    // Select the corresponding option in the "Alignment" <select>.
                    jq('#classes', document).val(classname);
                    break;

                default:
                    // Keep track of custom CSS classes so we can inject them
                    // back into the element later.
                    self.current_classes.push(classname);
                    break;
            }
        });

        scaled_image = this.parseImageScale(selected_node.attr("src"));

        // Update the dimensions <select> with the corresponding value.
        jq('#dimensions', document).val(scaled_image.scale);

        if (scaled_image.url.indexOf('resolveuid/') > -1) {
            /** Handle UID linked image **/

            current_uid = scaled_image.url.split('resolveuid/')[1];

            // Fetch the information about the UID linked image.
            jq.ajax({
                'url': this.editor.settings.portal_url + '/portal_tinymce/tinymce-getpathbyuid?uid=' + current_uid,
                'dataType': 'text',
                'type': 'GET',
                'success': function (text) {
                    // Store the absolute URL to the UID referenced image
                    self.current_url = self.getAbsoluteUrl(self.editor.settings.document_base_url, text);
                    // Store the image link as UID or full URL based on policy
                    self.current_link = self.editor.settings.link_using_uids ? scaled_image.url : self.current_url;

                    self.getFolderListing(self.getParentUrl(self.current_url), 'tinymce-jsonimagefolderlisting');
                }
            });
        } else {
            /** Handle directly linked image **/
            this.current_link = this.getAbsoluteUrl(this.editor.settings.document_base_url, scaled_image.url);
            this.getFolderListing(this.getParentUrl(this.current_link), 'tinymce-jsonimagefolderlisting');
        }
    } else {
        /** The image dialog was opened to add a new image. **/
        this.getCurrentFolderListing();
    }
};

/**
 * Parses the image scale (dimensions) from the given URL.
 *
 * The scale URLs used by plone.app.imaging are of the form
 *
 *   http://server.com/some-image.png/@@images/<field>/<scale>
 *
 * where <field> denotes the particular field containing the image and <scale>
 * identifies the particular image scale.
 *
 * For backward compatibility the previous form of image scale URLs is also
 * supported, but only for the "image" field, e.g.
 *
 *   http://server.com/some-image/image_<scale>
 *
 * where <scale> again denotes the particular image scale.
 *
 * Returns an object with the base URL to the image and another relative URL
 * to the image scale, e.g.
 *
 * { 'url': 'http://server.com/some-image',
 *   'scale' : '@@images/image/thumb' }
 *
 * The 'scale' key will always contain the plone.app.imaging type of scale
 * regardless of the original form, effectively rewriting everything to use
 * the @@images view.
 *
 * @param url URL to a possible scaled image.
 */
ImageDialog.prototype.parseImageScale = function (url) {
    var parts,
        last_part,
        scale_pos,
        parsed = {
            "url": url,
            "scale": ""
        };

    if (url.indexOf('/') > -1) {
        parts = url.split('/');
        last_part = parts[parts.length - 1];

        if (last_part.indexOf('image_') > -1) {
            // This is an old-style scale URL. We'll translate the scale to
            // the form used by plone.app.imaging.
            parsed.scale = "@@images/image/" + parts.pop().substring(6);
            parsed.url = parts.join("/");
        } else {
            scale_pos = url.search(/@@images\/[^\/]+\/.+/);
            if (scale_pos > -1) {
                // This is a new style URL
                parsed.url = url.substring(0, scale_pos - 1);
                parsed.scale = url.substring(scale_pos);
            }
        }
    }

    return parsed;
};

/**
 * Returns the URL of the currently selected image.
 *
 */
ImageDialog.prototype.getSelectedImageUrl = function () {
    // First, try to get the URL corresponding to the image that the user
    // selected in the center pane.
    // TODO: User is also able to select an image from the thumbnails view so
    //       it is important that the event handler there also updates the
    //       radio button input so that the selector below will work.
    var href = jq.trim(jq('input:radio[name=internallink]:checked', document).val());

    if (href === '') {
        // TODO: Is this branch necessary anymore?
        // The user didn't select an image from the center pane.  So we
        // default to the URL for the thumbnail image in the right pane.
        href = jq.trim(this.thumb_url);
        if (href !== '') {
            href = this.parseImageScale(href).url;
        }
    }

    return href;
};

/**
 * Handle inserting the selected image into the DOM of the editable area.
 *
 */
ImageDialog.prototype.insert = function () {
    var attrs,
        selected_node = this.editor.selection.getNode(),
        href = this.getSelectedImageUrl(),
        dimension,
        classes;

    this.tinyMCEPopup.restoreSelection();

    // Fixes crash in Safari
    if (tinymce.isWebKit) {
        this.editor.getWin().focus();
    }

    // Append the image scale to the URL if a valid selection exists.
    dimension = jq('#dimensions', document).val();
    if (dimension !== "") {
        href += '/' + dimension;
    }

    // Pass-through classes
    classes = [].concat(this.current_classes);
    // Alignment class
    classes.push(jq.trim(jq('#classes', document).val()));
    // Image captioning
    if (this.editor.settings.allow_captioned_images && jq('#caption', document).get(0).checked) {
        classes.push('captioned');
    }

    attrs = {
        'src' : href,
        'class' : classes.join(' ')
    };

    if (selected_node && selected_node.nodeName.toUpperCase() === 'IMG') {
        // Update an existing <img/> element
        this.editor.dom.setAttribs(selected_node, attrs);
    } else {
        // Create a new <img/> element.
        this.editor.execCommand('mceInsertContent', false, '<img id="__mce_tmp" />', {skip_undo : 1});
        this.editor.dom.setAttribs('__mce_tmp', attrs);
        this.editor.dom.setAttrib('__mce_tmp', 'id', '');
        this.editor.undoManager.add();
    }

    // Update the Description of the image
    jq.ajax({
        'url': jq('#description_href', document).val() + '/tinymce-setDescription',
        'type': 'POST',
        'data': {
            'description': encodeURIComponent(jq('#description', document).val())
        }
    });

    this.tinyMCEPopup.close();
};

/**
 * Activates and disables the search feature based on user input.
 */
ImageDialog.prototype.checkSearch = function (e) {
    var el = jq('#searchtext', document),
        len = el.val().length;

    // Activate search when we have enough input and either livesearch is
    // enabled or the user explicitly pressed Enter.
    if (len >= 3 && (this.tinyMCEPopup.editor.settings.livesearch || e.keyCode === 13)) {
        this.is_activated_search = true;
        this.getFolderListing(this.tinyMCEPopup.editor.settings.navigation_root_url, 'tinymce-jsonimagesearch');
        jq('#upload', document)
            .attr('disabled', true)
            .fadeTo(1, 0.5);
        jq('#internalpath', document).prev().text(this.labels.label_search_results);
    }

    // Disable search when we have no input or the user explicitly pressed the
    // Escape key.
    if ((len === 0 && this.is_activated_search) || e.keyCode === 27) {
        el.val('');
        this.is_activated_search = false;
        this.getCurrentFolderListing();
        jq('#upload', document)
            .attr('disabled', false)
            .fadeTo(1, 1);
        jq('#internalpath', document).prev().text(this.labels.label_internal_path);
    }
};

/**
 * Updates the details pane on the right by fetching image information from
 * the backend.
 *
 * After successful retrieval the right side pane will be updated with a
 * thumbnail of the selected image with information about the caption,
 * alignment and scale.
 *
 * @param image_url URL of the image to fetch.
 */
ImageDialog.prototype.setDetails = function (image_url) {
    var self = this,
        /**
         * Pretty-prints a human readable title for a image scale.
         */
        scale_title = function (scale) {
            if (scale.size[0]) {
                return scale.title + ' (' + scale.size[0] + 'x' + scale.size[1] + ')';
            } else {
                return scale.title;
            }
        };

    this.thumb_url = '';

    jq.ajax({
        'url': image_url + '/tinymce-jsondetails',
        'type': 'POST',
        'dataType': 'json',
        'success': function (data) {
            var dimension = jq('#dimensions', document).val(),
                dimensions;

            // Add the thumbnail image to the details pane.
            if (data.thumb !== "") {
                jq('#previewimagecontainer', document)
                    .empty()
                    .append(jq('<img/>').attr({'src': data.thumb}));
                // Save the thumbnail URL for later use.
                self.thumb_url = data.thumb;
            }

            jq('#description', document).val(data.description);
            jq('#description_href', document).val(image_url);

            // Repopulate the <option>s in the dimensions <select> element.
            if (data.scales) {
                dimensions = jq('#dimensions', document).empty();

                jq.each(data.scales, function () {
                    var scale = this,
                        option = jq('<option/>')
                            .attr({'value': scale.value})
                            .text(scale_title(scale));

                    if (option.val() === dimension) {
                        option.attr({'selected': 'selected'});
                    }
                    option.appendTo(dimensions);
                });
            }
            self.displayPreviewPanel();

            // select radio button in folder listing and mark selected image
            jq('input:radio[name=internallink][value!=' + image_url + ']', document).parent('.item').removeClass('current');
            jq('input:radio[name=internallink][value=' + image_url + ']', document)
                .attr('checked', true).parent('.item').addClass('current');

            self.current_url = image_url;
            self.current_link = self.editor.settings.link_using_uids ? data.uid_url : image_url;

        }
    });
};

/**
 * Utility method to update the middle pane with the current context listing.
 */
ImageDialog.prototype.getCurrentFolderListing = function () {
    this.getFolderListing(this.editor.settings.document_base_url, 'tinymce-jsonimagefolderlisting');
};


/**
 * Updates the center pane with a listing of content from the given context.
 *
 * @param context_url URL of the context where the request will be made
 * @param method Name of the backed view to query
 */
ImageDialog.prototype.getFolderListing = function (context_url, method) {
    var self = this;

    // store this for view type refreshing
    this.folderlisting_context_url = context_url
    this.folderlisting_method = method

    jq.ajax({
        'url': context_url + '/' + method,
        'type': 'POST',
        'dataType': 'json',
        'data': {
            'searchtext': encodeURIComponent(jq('#searchtext', document).val()),
            'rooted': this.editor.settings.rooted ? 'True' : 'False',
            'document_base_url': encodeURIComponent(this.editor.settings.document_base_url)
            },
        'success': function (data) {
            var html = [],
                len,
                current_uid,
                item_number = 0,
                folder_html = [],
                item_html = [],
                thumb_name = self.editor.settings.thumbnail_size[0],
                thumb_width = self.editor.settings.thumbnail_size[1],
                thumb_height = self.editor.settings.thumbnail_size[2],
                col_items_number = self.editor.settings.num_of_thumb_columns;

            if (data.items.length === 0) {
                html.push(self.labels.label_no_items);
            } else {
                jq.each(data.items, function (i, item) {
                    if (item.url === self.current_link && self.editor.settings.link_using_uids) {
                        self.current_link = 'resolveuid/' + item.uid;
                    }
                    if (item.is_folderish) {
                        jq.merge(folder_html, [
                            '<div class="list item folderish ' + (i % 2 === 0 ? 'even' : 'odd') + '">',
                                '<img src="img/arrow_right.png" />',
                                '<img src="' + item.icon +  '"/>',
                                '<a href="' + item.url + '" class="folderlink contenttype-' + item.normalized_type + '">',
                                    item.title,
                                '</a>',
                            '</div>'
                        ]);
                    } else {
                        switch (jq('#general_panel .legend .current', document).attr('id')) {
                            // TODO: use jquery dom to be sure stuff is closed
                            case 'listview':
                                jq.merge(item_html, [
                                    '<div class="item list ' + (i % 2 === 0 ? 'even' : 'odd') + '" title="' + item.description + '">',
                                        '<input href="' + item.url + '" ',
                                            'type="radio" class="noborder" style="margin: 0; width: 16px" name="internallink" value="',
                                            self.editor.settings.link_using_uids ? 'resolveuid/' + item.uid : item.url,
                                            '"/> ',
                                        '<img src="' + item.icon + '" /> ',
                                        '<span class="contenttype-' + item.normalized_type + '">' + item.title + '</span>',
                                    '</div>'
                                ]);
                                break;
                            case 'thumbview':
                                if (item_number % col_items_number === 0) {
                                    item_html.push('<div class="row">');
                                }
                                jq.merge(item_html, [
                                        '<div class="width-1:' + col_items_number + ' cell position-' + item_number % col_items_number * (16 / col_items_number) + '">',
                                            '<div class="thumbnail item ' + (i % 2 === 0 ? 'even' : 'odd') + '" title="' + item.description +  '">',
                                                '<div style="width: ' + thumb_width + 'px; height: ' + thumb_height + 'px" class="thumb">',
                                                    '<img src="' + item.url + '/@@images/image/' + thumb_name + '" alt="' + item.title + '" />',
                                                '</div>',
                                                '<p>' + item.title + '</p>',
                                                '<input href="' + item.url + '" ',
                                                    'type="radio" class="noborder" name="internallink" value="',
                                                    self.editor.settings.link_using_uids ? 'resolveuid/' + item.uid : item.url,
                                                    '"/> ',
                                            '</div>',
                                        '</div>'
                                        ]);
                                if (item_number % col_items_number === col_items_number - 1) {
                                    item_html.push('</div>');
                                }
                                item_number++;
                        }
                    }

                });
            }
            jq.merge(html, folder_html);
            jq.merge(html, item_html);
            jq('#internallinkcontainer', document).html(html.join(''));

            // shortcuts
            if (method !== 'tinymce-jsonimagesearch' && self.editor.settings.image_shortcuts_html.length) {
                jq('#internallinkcontainer', document).prepend('<div class="browser-separator"><img src="img/arrow_down.png"><strong>' + self.labels.label_browser + '</strong></div>');
                jq.each(self.editor.settings.image_shortcuts_html, function () {
                    jq('#internallinkcontainer', document).prepend('<div class="item list shortcut">' + this + '</div>');
                });
                jq('#internallinkcontainer', document).prepend('<div id="shortcuts" class="browser-separator"><img src="img/arrow_down.png"><strong>' + self.labels.label_shortcuts + '</strong></div>');
                jq('#shortcuts', document).click(function() {
                    jq('#internallinkcontainer .shortcut', document).toggle();
                });
            }

            // disable insert until we have selected an item
            jq('#insert', document).attr('disabled', true).fadeTo(1, 0.5);

            // make rows clickable
            jq('#internallinkcontainer div.item', document).click(function() {
                var el = jq(this),
                    checkbox = el.find('input');
                if (checkbox.length) {
                    checkbox.click();
                } else {
                    el.find('a').click();
                }
            });

            // breadcrumbs
            html = [];
            len = data.path.length;
            jq.each(data.path, function (i, item) {
                if (i > 0) {
                    html.push(" &rarr; ");
                }
                html.push('<img src="' + item.icon + '" /> ');
                if (i === len - 1) {
                    html.push(item.title);
                } else {
                    html.push('<a href="' + item.url + '">' + item.title + '</a>');
                }

            });
            jq('#internalpath', document).html(html.join(''));

            // folder link action
            jq('#internallinkcontainer a, #internalpath a', document).click(function(e) {
                e.preventDefault();
                e.stopPropagation();
                self.getFolderListing(jq(this).attr('href'), 'tinymce-jsonimagefolderlisting');
            });
            // item link action
            jq('#internallinkcontainer input:radio', document).click(function (e) {
                e.preventDefault();
                e.stopPropagation();
                self.setDetails(jq(this).attr('href'));
            });

            // Make the image upload form upload the image into the current container.
            jq('#upload_form', document).attr('action', context_url + '/tinymce-upload');

            if (self.current_link !== "") {
                if (self.current_link.indexOf('resolveuid/') > -1) {
                    current_uid = self.current_link.split('resolveuid/')[1];
                    jq.ajax({
                        'url': self.editor.settings.portal_url + '/portal_tinymce/tinymce-getpathbyuid?uid=' + current_uid,
                        'dataType': 'text',
                        'success': function(text) {
                            self.setDetails(self.getAbsoluteUrl(self.editor.settings.document_base_url, text));
                        }
                        // TODO: handle 410 (image was deleted)
                    });
                } else {
                    self.setDetails(self.current_link);
                }
            }

            // Check if allowed to upload
            if (data.upload_allowed) {
                jq('#upload', document).show();
            } else {
                jq('#upload', document).hide();
            }

        }
    });
};

/**
 * Returns a URL to the parent (container) of the given URL.
 *
 * @param url URL with at least a single path component.
 */
ImageDialog.prototype.getParentUrl = function(url) {
    var url_array = url.split('/');
    url_array.pop();
    return url_array.join('/');
};

/**
 * Returns an absolute URL based on a base url and a possibly relative link.
 *
 * If the given link is already an absolute URL it will be returned
 * unmodified, otherwise it will be joined with the base URL with any parent
 * references (..) factored out.
 *
 * @param base The base URL
 * @param link The link to calculate an absolute URL for
 */
ImageDialog.prototype.getAbsoluteUrl = function (base, link) {
    var base_array,
        link_array,
        item;

    if ((link.indexOf('http://') > -1) || (link.indexOf('https://') > -1) || (link.indexOf('ftp://') > -1)) {
        return link;
    }

    base_array = base.split('/');
    link_array = link.split('/');

    // Remove document from base url
    base_array.pop();

    while (link_array.length > 0) {
        item = link_array.shift();
        if (item === ".") {
            // Do nothing
            jq.noop();
        } else if (item === "..") {
            // Remove leave node from base
            base_array.pop();
        } else {
            // Push node to base_array
            base_array.push(item);
        }
    }

    return base_array.join('/');
};

ImageDialog.prototype.displayUploadPanel = function() {
    jq('#general_panel', document).width(530);
    jq('#addimage_panel', document).removeClass('hide');
    jq('#details_panel', document).addClass("hide");
    jq('#internallinkcontainer input', document).attr('checked', false);
    jq('#upload, #insert', document).attr('disabled', true).fadeTo(1, 0.5);
};

ImageDialog.prototype.displayPreviewPanel = function() {
    jq('#general_panel', document).width(530);
    jq('#addimage_panel', document).addClass('hide');
    jq('#details_panel', document).removeClass("hide");
    jq('#upload', document).attr('disabled', false).fadeTo(1, 1);
    jq('#insert', document).attr('disabled', false).fadeTo(1, 1);
};

ImageDialog.prototype.hidePanels = function() {
    jq('#general_panel', document).width(790);
    jq('#addimage_panel', document).addClass('hide');
    jq('#details_panel', document).addClass("hide");
    jq('#upload', document).attr('disabled', false).fadeTo(1, 1);
};


var imgdialog = new ImageDialog(tinyMCEPopup);
tinyMCEPopup.onInit.add(imgdialog.init, imgdialog);
