tinyMCEPopup.requireLangPack();

var PasteTextDialog = {
	init : function() {
	},

	insert : function() {
		var h = tinyMCEPopup.dom.encode(document.getElementById('content').value), lines;

		// Convert linebreaks into paragraphs
		if (document.getElementById('linebreaks').checked) {
			lines = h.split(/\r?\n/);
			if (lines.length > 1) {
				h = '';
				tinymce.each(lines, function(row) {
					h += '<p>' + row + '</p>';
				});
			}
		}

		tinyMCEPopup.editor.execCommand('mceInsertClipboardContent', false, h);
		tinyMCEPopup.close();
	}
};

tinyMCEPopup.onInit.add(PasteTextDialog.init, PasteTextDialog);
