High priority
=============

* https://dev.plone.org/ticket/13121

* https://dev.plone.org/ticket/13076

* We should probably forward-port
  https://github.com/plone/Products.TinyMCE/commit/9fb8b4d9a71a7db7089758d570376cf0a52e4b0b
  from master

* The "definition list" feature does not seem to work. It creates the list and
  One can enter the <dt>, but when we hit enter it does not switch to editing
  a <dd>

* Review everything was merged from 1.2.x branch

* Align full does not work

* Select special character: not sure if the current selected camera should
get a highlight or other visual cue.

* pagebreak is only inserting <!-- pagebreak -->

* show/hide visual control characters (the pi) doesn't do anything

* insert/edit attributes. left to right/right to left adds dir attribute to
  a paragraph, but language doesn't do anything

* Fonts to big in the dialogues:

  *  Paste from word: font to big, insert/cancel buttons disappear

  *  resize the smiley widget so it's big enough for 4x4 smileys

  *  Insert table  Summary field is difficult to edit, wrong layout

Normal priority
---------------

* Instead of having external tinymce repository at src/tinymce, use git submodule

* Bug: inserting flash video does not work
  https://github.com/iElectric/Products.TinyMCE/issues/23

* Insert/embed media Type does not pull in the correct translations
  (media_dlg.flash). Inserting iFrame does not work.

* External link preview throws error: Refused to display document because
  display forbidden by X-Frame-Options.
  Solution: just add a link to open the page in new window

* Always use resolveuids internally, cherry-pick from
  hexagonit: ce432622ea357f426239573bf6042b8f80804393

* Last week I discovered a problem with certain custom TinyMCE-plugins and
  Products.TinyMCE 1.3-beta1: if a custom plugin defines an alternative path
  (eg. plonetemplates|/++resource++collective.tinymcetemplates.plugin/editor_plugin.js),
  then this plugin will not be found by TinyMCE. This feature works correctly
  in Products.TinyMCE 1.2.10. Is this a known problem?

* Close https://dev.plone.org/ticket/10039 (add tests),
  https://dev.plone.org/ticket/10571

* configure Jenkins tests with Plone 3.3, 4.1, 4.2 and 4.3

* https://dev.plone.org/ticket/11973

* Bug: opera browser problems


Future releases
---------------

* Handle everything with UIDs internally (delete control panel option)

* Shortcut html5 placeholder fallback http://dev.plone.org/plone/ticket/10394

* Provide link to image in image browser

* "Edit without visual editor" does not provide back button image
  https://dev.plone.org/ticket/10722

* TinyMCE doesn't display workflow state information about content in popups
  https://dev.plone.org/plone/ticket/10858 .state-private

* Do security audit (class security, CSRF tokens)

* Handle error in UID

* Top alignment, of all rows in table, is lost when saving
  (http://dev.plone.org/ticket/10300)

* Save button in toolbar is missing in Dexterity

* Search results should include path information

* Paste as plain text as default:
  http://stackoverflow.com/questions/2695731/how-to-make-tinymce-paste-in-plain-text-by-default

* Fill in plone bug/features and link them to changes

* Add links without text being selected first
  https://dev.plone.org/plone/ticket/9908

* External images upload support (UI already done)
  https://dev.plone.org/plone/ticket/10039

* Make formunload.js work again

* Backspace in content browser should move up one directory

* Description preview should be bigger, add title 

* Provide easy way to change default "browse" folder
  http://stackoverflow.com/questions/5821362/making-tinymce-image-pick-dialog-point-to-a-default-folder-on-plone

* Rewrite plonebrowser with forms/interfaces

* Language files are misplaced -> "Source" tab not appearing in media plugin -
  i18n problems

* Add http://pypi.python.org/pypi/zopyx.tinymceplugins.tinyautosave/ implement
  "main repository"

* Drag & drop support in image&link browser

* Multi insert image/link

* Add setting where does content browser starts in (current folder, ...)

* List: refactor to plone.app.tinymce and plone.app.visualeditors


To be reported upstream
-----------------------

* Select multiple lines of unordered list, and try to change the style for
  them. You can select it from the style dorpdown, but nothing is applied.
  (list_style.png) This is due to the next bug:

* Create an unordered list, add 3 items to it, select the second and click on
  unordered list. The selected line is no longer a list, but if you click it
  again, it will be a new unordered list, and not a part of the existing one.
  If there is a list right before the selected one, then it should be part of
  it.

* Table - bottom markers do not take padding into account. (table_marker.png)

* Table - Multiple cell selection does not work. (merge_cells.png)

* https://github.com/hexagonit/tinymce/cofeatures/mmit/f063d53f97c3afd9eb55f38d62034c50af65955e

* fixes in skins/tinymce/tiny_mce_src.js

* fixes in skins/tinymce/plugins/paste/pastetext.html.pt and
  skins/tinymce/plugins/paste/js/pastetext.js
