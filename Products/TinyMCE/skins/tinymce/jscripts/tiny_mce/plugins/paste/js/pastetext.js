tinyMCEPopup.requireLangPack();

function saveContent() {
	if (document.forms[0].htmlSource.value == '') {
		tinyMCEPopup.close();
		return false;
	}

	tinyMCEPopup.execCommand('mcePasteText', false, {
		html : document.forms[0].htmlSource.value,
		linebreaks : document.forms[0].linebreaks.checked
	});

	tinyMCEPopup.close();
}

function onLoadInit() {
	tinyMCEPopup.resizeToInnerSize();

	// Remove Gecko spellchecking
	if (tinymce.isGecko)
		document.body.spellcheck = tinyMCEPopup.getParam("gecko_spellcheck");
}

tinyMCEPopup.onInit.add(onLoadInit);