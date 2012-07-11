High priority
=============

* add 1.3 GS profile to plone.app.upgrades for Plone 4.3

* Merge (we should restrict upload of images to certain extensions and notify
  user at wrong outcome)
  https://github.com/plone/Products.TinyMCE/commit/96d7415987bb1e2dc1283d02e8648fef85499fe7

* Merge
  https://github.com/plone/Products.TinyMCE/commit/6aaf14e7e66592fce118d2050e699d66e14b201c

* The new link/image dialog implementation seems to function fine and have
  feature paarity with the old one, but there are a number of visual glitches
  which make it look jarring and unfinished:
    1. Something is too wide so the Link Browser floats below, mostly off
    screen.
    2. The text is too big compared to elsewhere in the theme.
    3. A different icon set is used than elsewhere in Plone. We should be
    consistent.
    4. The standard Plone icons for content types are not aligned with their
    content item.
    5. The buttons are a weird style that is different from elsewhere in
    Plone. We should be consistent. (This is true for all tinymce dialogs,
    not just the custom Plone ones.)
    6. The "Advanced options" page has a blank dropdown of unclear function.

* The "definition list" feature does not seem to work. It creates the list and
  One can enter the <dt>, but when we hit enter it does not switch to editing
  a <dd> Needs to be updated to not register the old resources when a Plone
  site is created.

* We should probably forward-port
  https://github.com/plone/Products.TinyMCE/commit/4937f74b8485c5800347c204385c3f0923b45e81
  and
  https://github.com/plone/Products.TinyMCE/commit/9fb8b4d9a71a7db7089758d570376cf0a52e4b0b
  from master

* Check all plugins/buttons

* Review everything was merged from 1.2.x branch

Normal priority
---------------

* Instead of having external tinymce repository at src/tinymce, use git submodule

* Bug: inserting flash video does not work
  https://github.com/iElectric/Products.TinyMCE/issues/23

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

* Fix tests in jenkins


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
