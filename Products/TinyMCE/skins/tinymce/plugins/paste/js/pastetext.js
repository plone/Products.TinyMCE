tinyMCEPopup.requireLangPack();

var PasteTextDialog = {
	init : function() {
	},

	insert : function() {
	    // Plone fix: rename the textarea to avoid conflicting with the main #content div
		var h = tinyMCEPopup.dom.encode(document.getElementById('mceTextPaste').value), lines;

		// Convert linebreaks into <br/> tags
		// Plone fix: turn double-linebreaks into paragraph tags
		if (document.getElementById('linebreaks').checked) {
			lines = h.split(/\r?\n\s*\r?\n/);
			if (lines.length > 1) {
				h = '';
				tinymce.each(lines, function(row) {
					h += '<p>' + row + '</p>';
				});
			}
			lines = h.split(/\r?\n/);
			if (lines.length > 1) {
				h = '';
				tinymce.each(lines, function(row) {
					h += '<br/>' + row;
				});
			}
		}

		tinyMCEPopup.editor.execCommand('mceInsertClipboardContent', false, {content : h});
		tinyMCEPopup.close();
	}
};

tinyMCEPopup.onInit.add(PasteTextDialog.init, PasteTextDialog);
