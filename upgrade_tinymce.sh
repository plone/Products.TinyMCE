set -e
root=$(dirname $0)
product_root=$root/Products/TinyMCE/
tinymce_root=$product_root/skins/tinymce/
tinymce_git_root=$root/src/tinymce/

echo "*** Building tinymce ..."
ant -s $tinymce_git_root/build.xml

echo "*** Cleaning old tinymce version ..."
rm -rf $tinymce_root/*

echo "*** Copying files ..."
cp -R $tinymce_git_root/jscripts/tiny_mce/* $tinymce_root/

echo "*** Removing unneeded files ..."
rm -rf $tinymce_root/classes
rm -rf $tinymce_root/themes/simple
rm -f $tinymce_root/{*prototype*,*jquery*,license.txt,tiny_mce_dev.js}

echo "*** Removing unneeded plugins ..."
rm -rf $tinymce_root/plugins/{advimage,advlink,example,fullpage,style,simple}

# plugins modifications
find $tinymce_root -name "*.html" | xargs rename -f s/html$/html.pt/
find $tinymce_root -name "*.htm" | xargs rename -f s/htm$/htm.pt/
find $tinymce_root -name "*_src.js" -delete

echo "*** Updating language files ..."
cd $product_root/utils/
#python wget-xml.py
python generate-po.py
python compile-mo.py
cd $root

echo "*** Done. Don't forget to update CHANGELOG and commit!"
