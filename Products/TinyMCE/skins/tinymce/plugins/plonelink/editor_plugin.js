/**
 * Plone link plugin based on advlink plugin.
 *
 * @author Rob Gietema
 */

(function() {
	tinymce.create('tinymce.plugins.PloneLinkPlugin', {
		init : function(ed, url) {
			this.editor = ed;

			// Register commands
			ed.addCommand('mceAdvLink', function() {
				var se = ed.selection;

				// No selection and not in link
				if (se.isCollapsed() && !ed.dom.getParent(se.getNode(), 'A'))
					return;

				ed.windowManager.open({
					file : url + '/plonelink.htm',
					width : 820 + parseInt(ed.getLang('advlink.delta_width', 0)),
					height : 470 + parseInt(ed.getLang('advlink.delta_height', 0)),
					inline : 1
				}, {
					plugin_url : url
				});
			});

			// Register buttons
			ed.addButton('link', {
				title : 'advlink.link_desc',
				cmd : 'mceAdvLink'
			});

			ed.addShortcut('ctrl+k', 'advlink.advlink_desc', 'mceAdvLink');

			ed.onNodeChange.add(function(ed, cm, n, co) {
				cm.setDisabled('link', co && n.nodeName != 'A');
				cm.setActive('link', n.nodeName == 'A' && !n.name);
			});
		},

		getInfo : function() {
			return {
				longname : 'Plone link',
				author : 'Rob Gietema',
				authorurl : 'http://plone.org',
				infourl : 'http://plone.org/products/tinymce',
				version : tinymce.majorVersion + "." + tinymce.minorVersion
			};
		}
	});

	// Register plugin
	tinymce.PluginManager.add('plonelink', tinymce.plugins.PloneLinkPlugin);
})();