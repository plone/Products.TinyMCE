/**
 * mctabs.js
 *
 * Copyright 2009, Moxiecode Systems AB
 * Released under LGPL License.
 *
 * License: http://tinymce.moxiecode.com/license
 * Contributing: http://tinymce.moxiecode.com/contributing
 */

function MCTabs() {
	this.settings = [];
	this.editor = tinyMCEPopup.editor;
	this.tinymce = tinyMCEPopup.getWin().tinymce;
	this.dom = tinyMCEPopup.dom;
	this.onChange = tinyMCEPopup.editor.windowManager.createInstance('tinymce.util.Dispatcher');
};

MCTabs.prototype.init = function(settings) {
	this.settings = settings;
};

MCTabs.prototype.getParam = function(name, default_value) {
	var value = null;

	value = (typeof(this.settings[name]) == "undefined") ? default_value : this.settings[name];

	// Fix bool values
	if (value == "true" || value == "false")
		return (value == "true");

	return value;
};

MCTabs.prototype.showTab =function(tab){
	var t = this;
	t.dom.addClass(tab,'current');

	var nodes = tab.childNodes;
	for (var i = 0; i < nodes.length; i++) t.dom.addClass(nodes[i], 'selected');
	
	tab.setAttribute("aria-selected", true);
	tab.setAttribute("aria-expanded", true);
	tab.tabIndex = 0;
};

MCTabs.prototype.hideTab =function(tab){
	var t=this;
	t.dom.removeClass(tab,'current');

	var nodes = tab.childNodes;
	for (var i = 0; i < nodes.length; i++) t.dom.removeClass(nodes[i], 'selected');

	tab.setAttribute("aria-selected", false);
	tab.setAttribute("aria-expanded", false);
	tab.tabIndex = -1;
};

MCTabs.prototype.showPanel = function(panel) {
	var t = this;
	t.dom.addClass(panel,'current');
	t.dom.show(panel);
	panel.setAttribute("aria-hidden", false);
};

MCTabs.prototype.hidePanel = function(panel) {
	var t=this;
	t.dom.removeClass(panel,'current');
	t.dom.hide(panel);
	panel.setAttribute("aria-hidden", true);
}; 

MCTabs.prototype.getPanelForTab = function(tabElm) {
	return tinyMCEPopup.dom.getAttrib(tabElm, "aria-controls");
};

MCTabs.prototype.displayTab = function(tab_id, panel_id, avoid_focus) {
	var panelContainerElm, tabContainerElm, t = this;

	/* tab dom node  */
	var tabElm = document.getElementById(tab_id);

	if (panel_id === undefined) {
		panel_id = t.getPanelForTab(tabElm);
	}

	/* tab content dom node */
	var panelElm= document.getElementById(panel_id);
	panelContainerElm = panelElm ? panelElm.parentNode : null;
	
	tabContainerElm = tabElm ? tabElm.parentNode : null;
	selectionClass = t.getParam('selection_class', 'current');

	if (tabElm && tabContainerElm) {
		var nodes = tabContainerElm.childNodes;

		// Hide all other tabs
		var nn = tabElm.nodeName;
		for (var i = 0; i < nodes.length; i++) {
			if (nodes[i].nodeName == nn) {
				t.hideTab(nodes[i]);
			}
		}

		// Show selected tab
		t.showTab(tabElm);
	}

	if (panelElm && panelContainerElm) {
		var nodes = panelContainerElm.childNodes;

		// Hide all other panels
		var nn = panelElm.nodeName;
		for (var i = 0; i < nodes.length; i++) {
			if (nodes[i].nodeName == nn)
				t.hidePanel(nodes[i]);
		}

		if (!avoid_focus) { 
			tabElm.focus();
		}

		// Show selected panel
		t.showPanel(panelElm);
	}
};

MCTabs.prototype.getAnchor = function() {
	var pos, url = document.location.href;

	if ((pos = url.lastIndexOf('#')) != -1)
		return url.substring(pos + 1);

	return "";
};


//Global instance
var mcTabs = new MCTabs();

tinyMCEPopup.onInit.add(function() {
	var tinymce = tinyMCEPopup.getWin().tinymce, dom = tinyMCEPopup.dom, each = tinymce.each;

	each(dom.select('div.tabs'), function(tabContainerElm) {
		var keyNav;

		dom.setAttrib(tabContainerElm, "role", "tablist"); 

		var items = tinyMCEPopup.dom.select('li', tabContainerElm);
		var action = function(id) {
			mcTabs.displayTab(id, mcTabs.getPanelForTab(id));
			mcTabs.onChange.dispatch(id);
		};

		each(items, function(item) {
			dom.setAttrib(item, 'role', 'tab');
			dom.bind(item, 'click', function(evt) {
				action(item.id);
			});
		});

		dom.bind(dom.getRoot(), 'keydown', function(evt) {
			if (evt.keyCode === 9 && evt.ctrlKey && !evt.altKey) { // Tab
				keyNav.moveFocus(evt.shiftKey ? -1 : 1);
				tinymce.dom.Event.cancel(evt);
			}
		});

		each(dom.select('a', tabContainerElm), function(a) {
			dom.setAttrib(a, 'tabindex', '-1');
		});

		keyNav = tinyMCEPopup.editor.windowManager.createInstance('tinymce.ui.KeyboardNavigation', {
			root: tabContainerElm,
			items: items,
			onAction: action,
			actOnFocus: true,
			enableLeftRight: true,
			enableUpDown: true
		}, tinyMCEPopup.dom);
	});
});