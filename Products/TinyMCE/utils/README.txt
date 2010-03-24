Updating tinymce.po files
------------------------
python wget-xml.py
change to utf-8 the xml declaration in ja.xml, ch.xml, zh.xml and ko.xml
python generate-po.py

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
