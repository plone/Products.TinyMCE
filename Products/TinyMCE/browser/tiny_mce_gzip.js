(function($, Patterns, undefined) {

  window.initTinyMCE = function(context) {

    $('textarea.mce_editable', context).each(function() {
      var $el = $(this),
          $field = $el.parents('.field'),
          tinymceActive = false,
          config = $.parseJSON($el.attr('data-mce-config')),
          $textFormatSelector = $('.fieldTextFormat > select', $field);

      $('.suppressVisualEditor', $field).hide();
      $textFormatSelector.bind('change', function(e) {
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

      if(!$textFormatSelector.length){
        // If there is no selector, honour the intent of the mce_editable
        // class on this textarea.
        $el.tinymce(config);
        tinymceActive = true;
      } else if ($textFormatSelector.val() === 'text/html') {
        // If there is a format selector, only initialise when it asks
        // for html.
        $el.tinymce(config);
        tinymceActive = true;
      }

    });
  };

  $(document).ready(function() {
    if (Patterns) {
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
