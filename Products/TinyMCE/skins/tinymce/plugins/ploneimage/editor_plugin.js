/**
 * $Id: editor_plugin_src.js 677 2008-03-07 13:52:41Z spocke $
 *
 * @author Moxiecode
 * @copyright Copyright © 2004-2008, Moxiecode Systems AB, All rights reserved.
 */

(function() {
	tinymce.create('tinymce.plugins.PloneImagePlugin', {
		init : function(ed, url) {
			// Register commands
			ed.addCommand('mcePloneImage', function() {
				// Internal image object like a flash placeholder
				if (ed.dom.getAttrib(ed.selection.getNode(), 'class').indexOf('mceItem') != -1)
					return;

				ed.windowManager.open({
					file : url + '/ploneimage.htm',
					width : 820 + parseInt(ed.getLang('ploneimage.delta_width', 0)),
					height : 470 + parseInt(ed.getLang('ploneimage.delta_height', 0)),
					inline : 1
				}, {
					plugin_url : url
				});
			});

			// Register buttons
			ed.addButton('image', {
				title : 'ploneimage.image_desc',
				cmd : 'mcePloneImage'
			});
		},

		getInfo : function() {
			return {
				longname : 'Plone image',
				author : 'Rob Gietema',
				authorurl : 'http://plone.org',
				infourl : 'http://plone.org/products/tinymce',
				version : tinymce.majorVersion + "." + tinymce.minorVersion
			};
		}
	});

	// Register plugin
	tinymce.PluginManager.add('ploneimage', tinymce.plugins.PloneImagePlugin);
})();