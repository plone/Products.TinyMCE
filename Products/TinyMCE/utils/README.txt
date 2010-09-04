Updating tinymce.po files
------------------------
python wget-xml.py
python generate-po.py

Go to the locales directory and execute:
for po in `find . -name "*.po"` ; do msgfmt -o `dirname $po`/`basename $po .po`.mo $po; done
and fix all errors.

Updating the langs js files
---------------------------
Check all checkbox on
http://tinymce.moxiecode.com/download_i18n.php
and download the tinymce_lang_pack.zip

cd skins/tinymce
unzip ~/tinymce_lang_pack.zip
mv plugins/advlink/langs/* plugins/plonelink/langs/
mv plugins/advimage/langs/* plugins/ploneimage/langs/
rm -rf plugins/advlink plugins/advimage plugins/style plugins/fullpage themes/simple
