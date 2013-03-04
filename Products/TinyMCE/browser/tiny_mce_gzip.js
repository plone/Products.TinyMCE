(function($, Patterns, undefined) {

  window.initTinyMCE = function(context) {

    $('textarea.mce_editable', context).each(function() {
      var el = $(this),
          config = $.parseJSON(el.attr('data-mce-config'));

      // TODO: for now we only hide options which are clearly not working right
      // now. i'm not really sure how this should be working.
      $('.suppressVisualEditor, .fieldTextFormat', el.parents('.field')).hide();

      // not the nicest way to put this here as usuall kittens will die
      // and ponies stop flying
      //
      // only relevant to tiles
      if (el.parents('form#add_tile').size() === 1 ||
          el.parents('form#edit_tile').size() === 1) {

        // filter out buttons we dont allow
        var buttons = [];
        $.each(config.buttons, function(i, button) {
          // probably it would be nice that the list of buttons below would be
          // possible to configure
          if ($.inArray(button, ["style", "bold", "italic", "justifyleft",
              "justifycenter", "justifyright", "justifyfull", "bullist",
              "numlist", "definitionlist", "outdent", "indent", "link",
              "unlink", "code"]) !== -1) {
              // not sure about "anchor", "fullscreen"
              buttons.push(button);
          }
        });
        config.buttons = buttons;
        config.theme_advanced_buttons1 = buttons.join(',');
        config.theme_advanced_buttons2 = '';
        config.theme_advanced_buttons3 = '';

        // copy css from top frame to content frame of tinymce
        // FIXME: its not copying style elements with css using @import
        var content_css = [];
        $('link,style', window.parent.document).each(function(i, item) {
          if ($.nodeName(item, 'link') && $(item).attr('href')) {
            content_css += ',' + $(item).attr('href');
          } else if ($.nodeName(item, 'style') && $(item).attr('src')) {
            content_css += ',' + $(item).attr('src');
          }
        });
        config.content_css = content_css;

        // max height is 8 rows
        el.attr('rows', '8');

      }

      // make initialization work in bootstrap modal
      var modal = el.parents('.modal');
      if (modal.size() !== 0) {

        if (modal.is(':visible')) {
          el.tinymce(config);
        } else {
          modal.on('shown', function() {
            el.tinymce(config);
          });
        }
        modal.on('hide', function() {
          tinyMCE.execCommand('mceRemoveControl', false, el.attr('id'));
        });

      // initialize tinymce outside modal
      } else {
        el.tinymce(config);
      }

    });

    // set Text Format dropdown untabbable for better UX
    // TODO: find a better way to fix this
    $('#text_text_format', context).attr('tabindex', '-1');
  }

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
