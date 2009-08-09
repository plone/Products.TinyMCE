/**
 * $Id: mctabs.js 758 2008-03-30 13:53:29Z spocke $
 *
 * Moxiecode DHTML Tabs script.
 *
 * @author Moxiecode
 * @copyright Copyright © 2004-2008, Moxiecode Systems AB, All rights reserved.
 */

function MCTabs() {
	this.settings = [];
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

MCTabs.prototype.displayTab = function(tab_id, panel_id) {
	var panelElm, panelContainerElm, tabElm, tabContainerElm, selectionClass, nodes, i;

	panelElm= document.getElementById(panel_id);
	panelContainerElm = panelElm ? panelElm.parentNode : null;
	tabElm = document.getElementById(tab_id);
	tabContainerElm = tabElm ? tabElm.parentNode : null;
	selectionClass = this.getParam('selection_class', 'current');

	if (tabElm && tabContainerElm) {
		nodes = tabContainerElm.childNodes;

		// Hide all other tabs
		for (i = 0; i < nodes.length; i++) {
			if (nodes[i].nodeName == "LI")
				nodes[i].firstChild.className = '';
		}

		// Show selected tab
		tabElm.firstChild.className = 'selected';
	}

	if (panelElm && panelContainerElm) {
		nodes = panelContainerElm.childNodes;

		// Hide all other panels
		for (i = 0; i < nodes.length; i++) {
			if (nodes[i].nodeName == "FIELDSET")
				nodes[i].style.display = 'none';
		}

		// Show selected panel
		panelElm.style.display = 'block';
	}
};

MCTabs.prototype.getAnchor = function() {
	var pos, url = document.location.href;

	if ((pos = url.lastIndexOf('#')) != -1)
		return url.substring(pos + 1);

	return "";
};

// Global instance
var mcTabs = new MCTabs();
