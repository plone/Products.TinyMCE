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

jQuery(function() {

    jQuery('textarea.mce_editable').tinymce({
            // Location of TinyMCE script
            script_url : '<tal:url tal:replace="string:${options/base_url}" />',

            mode : "exact",
            elements : this.id,
            strict_loading_mode : true,
            theme : "advanced",
            language : "<tal:lang tal:replace='options/config/language' />",
            skin : "plone",
            inlinepopups_skin : "plonepopup",
            plugins : "<tal:lang tal:replace='options/plugins' />",
            // Find out if ieSpell requires gecko spellchecker...
            gecko_spellcheck : "<tal:spell tal:replace="python:options['config']['libraries_spellchecker_choice'] == 'browser' and 'true' or 'false'" />",

            atd_rpc_id : "<tal:lang tal:replace='options/config/atd_rpc_id' />",
            atd_rpc_url : "<tal:lang tal:replace='options/config/atd_rpc_url' />",
            atd_show_types : "<tal:lang tal:replace='options/config/atd_show_types' />",
            atd_ignore_strings : "<tal:lang tal:replace='options/config/atd_ignore_strings' />",

            labels :  <tal:lang tal:replace='options/labels' />,
            theme_advanced_styles :  '<tal:lang tal:replace="options/styles" />',
            theme_advanced_buttons1 : "<tal:lang tal:replace="python:options['toolbars'][0]" />",
            theme_advanced_buttons2 : "<tal:lang tal:replace="python:options['toolbars'][1]" />",
            theme_advanced_buttons3 : "<tal:lang tal:replace="python:options['toolbars'][2]" />",
            theme_advanced_buttons4 : "<tal:lang tal:replace="python:options['toolbars'][3]" />",
            theme_advanced_toolbar_location : "<tal:lang tal:replace='options/config/toolbar_location' />",
            theme_advanced_toolbar_align : "left",
            theme_advanced_path_location : "<tal:lang tal:replace='options/config/path_location' />",
            theme_advanced_path : false,
            theme_advanced_resizing : "<tal:lang tal:replace='options/config/resizing' />", 
            theme_advanced_resizing_use_cookie : "<tal:lang tal:replace='options/config/resizing_use_cookie' />",
            theme_advanced_resize_horizontal : "<tal:lang tal:replace='options/config/resize_horizontal' />",
            theme_advanced_source_editor_width : "<tal:lang tal:replace='options/config/editor_width' />",
            theme_advanced_source_editor_height : "<tal:lang tal:replace='options/config/editor_height' />",

            table_styles : "<tal:lang tal:replace="python:';'.join(options['config']['table_styles'])" />",
            table_firstline_th : true,
            directionality : "<tal:lang tal:replace='options/config/directionality' />",
            entity_encoding : "<tal:lang tal:replace='options/config/entity_encoding' />",
            content_css : "<tal:lang tal:replace='options/config/content_css' />",
            body_class : "documentContent",
            body_id : "content",
            document_url : "<tal:lang tal:replace='options/config/document_url' />",
            portal_url : "<tal:lang tal:replace='options/portal_url' />",
            navigation_root_url : "<tal:lang tal:replace='options/config/navigation_root_url' />",
            livesearch : "<tal:lang tal:replace='options/config/livesearch' />",
            valid_elements : "<tal:lang tal:replace='options/valid_elements' />",
            valid_inline_styles : "<tal:lang tal:replace="python:','.join(options['config']['valid_inline_styles'])" />",
            link_using_uids : "<tal:lang tal:replace='options/config/link_using_uids' />",
            allow_captioned_images :"<tal:lang tal:replace='options/config/allow_captioned_images' />",
            rooted : "<tal:lang tal:replace='options/config/rooted' />",
/*     XXX       document_base_url : this.getBase(),
            link_shortcuts_html : this.widget_config.link_shortcuts_html,
            image_shortcuts_html : this.widget_config.image_shortcuts_html,
            num_of_thumb_columns : this.widget_config.num_of_thumb_columns,
            thumbnail_size : this.widget_config.thumbnail_size, */
            force_span_wrappers : true,
            fix_list_elements : false
    });
});
