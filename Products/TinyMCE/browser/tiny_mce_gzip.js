(function($, Patterns, undefined) {

  window.initTinyMCE = function(context) {

    $('textarea.mce_editable', context).each(function() {
      var $el = $(this),
          $field = $el.parents('.field'),
          tinymceActive = false,
          config = $.parseJSON($el.attr('data-mce-config'));

      $('.suppressVisualEditor', $field).hide();
      $('.fieldTextFormat > select', $field).bind('change', function(e) {
        e.stopPropagation();

        if ($(e.target).val() === 'text/html') {
          // only activate if it unactive
          if (!tinymceActive) {
            $el.tinymce(config);
            tinymceActive = true;
          }

        // only deactivate if active
        } else if (tinymceActive) {
          tinyMCE.execCommand('mceRemoveControl', false, $el.attr('id'));
          tinymceActive = false;
        }

      // set Text Format dropdown untabbable for better UX
      }).attr('tabindex', '-1');

      if ($('.fieldTextFormat > select', $field).val() === 'text/html') {
        $el.tinymce(config);
        tinymceActive = true;
      }

      // Load TinyMCE also if there's no text format dropdown and the vaue is text/html
      if ($('input[name="text_text_format"]', $field).val() === 'text/html') {
        $el.tinymce(config);
        tinymceActive = true;
      }

    });
  };

  $(document).ready(function() {
    if (Patterns) {
      console.log('tinymce!!!');
      var PloneTinyMCE = Patterns.extend({
        name: 'plone-tinymce',
        jqueryPlugin: 'ploneTinymce',
        init: function() {
          initTinyMCE(this.$el.parent());
        }
      });
    } else {
      $(document).ready(function() {
        window.initTinyMCE(document);
      });
    }
  });

}(window.jQuery, window.Patterns));
