/**
 * Based on "TinyMCE Compressor PHP" from MoxieCode.
 *
 * http://tinymce.moxiecode.com/
 *
 * Copyright (c) 2008 Jason Davies
 * Licensed under the terms of the MIT License (see LICENSE.txt)
 *
 * Usage: copy this file into the same directory as tiny_mce.js and change
 * settings.page_name below to match your tinymce installation as appropriate.
 */

jQuery(function($) {
    var conf = $.extend({
            elements: this.id
        },
        <tal:url tal:content="structure options/tinymce_json_config" />);
    $('textarea.mce_editable').tinymce(conf);
});
