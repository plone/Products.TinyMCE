Updating tinymce.po files
------------------------
python wget-xml.py
python generate-po.py

Go to the locales directory and execute:
for po in `find . -name "*.po"` ; do msgfmt -o `dirname $po`/`basename $po .po`.mo $po; done
and fix all errors.