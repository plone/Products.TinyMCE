tinyMCEPopup.requireLangPack();

function saveContent() {
	var html = document.getElementById("frmData").contentWindow.document.body.innerHTML;

	if (html == ''){
		tinyMCEPopup.close();
		return false;
	}

	tinyMCEPopup.execCommand('mcePasteWord', false, html);
	tinyMCEPopup.close();
}

function onLoadInit() {
	tinyMCEPopup.resizeToInnerSize();

	// Fix for endless reloading in FF
	window.setTimeout(createIFrame, 10);
}

function createIFrame() {
	document.getElementById('iframecontainer').innerHTML = '<iframe id="frmData" name="frmData" class="input-border" src="blank.htm" height="261" width="398" frameborder="0" style="background-color:#FFFFFF; width:100%;" dir="ltr" wrap="soft"></iframe>';
}

var wHeight=0, wWidth=0, owHeight=0, owWidth=0;

function initIframe(doc) {
	var dir = tinyMCEPopup.editor.settings.directionality;

	doc.body.dir = dir;

	// Remove Gecko spellchecking
	if (tinymce.isGecko)
		doc.body.spellcheck = tinyMCEPopup.getParam("gecko_spellcheck");
}

tinyMCEPopup.onInit.add(onLoadInit);
