/**
 * Based on "TinyMCE Compressor PHP" from MoxieCode.
 *
 * http://tinymce.moxiecode.com/
 *
 * Copyright (c) 2008 Jason Davies
 * Licensed under the terms of the MIT License (see LICENSE.txt)
 *
 */

jQuery(function($) {
  <tal:loop repeat="conf options/tinymce_json_config">
    $('#<tal:fieldname tal:replace="conf/fieldname" />').tinymce(
      <tal:url tal:replace="structure conf/config" />);

    var text_format = $('#<tal:fieldname tal:replace="conf/fieldname" />_text_format');
  
    text_format.change( function() {

        var editor = $('#<tal:fieldname tal:replace="conf/fieldname" />').tinymce()

        var mimetype = $('option:selected' ,this).val();
        if (mimetype.indexOf('html') === -1) {  
//        XXX don't hide editor. for some reason the field value
//        does not get extracted any more.
//        editor.hide()
        } else {
            editor.show()
        }

    });
  </tal:loop>

    // set Text Format dropdown untabbable for better UX
    // TODO: find a better way to fix this
    $('#text_text_format').attr('tabindex', '-1');
});
