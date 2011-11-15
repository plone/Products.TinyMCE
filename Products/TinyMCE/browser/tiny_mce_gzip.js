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
  <tal:loop repeat="conf options/tinymce_json_config">
    $('textarea#<tal:fieldname tal:replace="conf/fieldname" />').tinymce(
      <tal:url tal:replace="structure conf/config" />);
  </tal:loop>

    // set Text Format dropdown untabbable for better UX
    // TODO: find a better way to fix this
    $('#text_text_format').attr('tabindex', '-1');
});
