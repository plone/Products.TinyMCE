set -e
#root=$(dirname $0)
root=$PWD
product_root=$root/Products/TinyMCE
tinymce_root=$product_root/skins/tinymce
tinymce_git_root=$root/src/tinymce

echo "*** Building tinymce ..."
ant -s $tinymce_git_root/build.xml

echo "*** Cleaning old tinymce version ..."
rm -rf $tinymce_root/*

echo "*** Copying files ..."
cp -R $tinymce_git_root/jscripts/tiny_mce/* $tinymce_root/

echo "*** Removing unneeded files ..."
rm -rf $tinymce_root/classes
rm -rf $tinymce_root/themes/simple
rm -f $tinymce_root/{*prototype*,license.txt,tiny_mce_dev.js,tiny_mce_jquery_src.js}

echo "*** Removing unneeded plugins ..."
rm -rf $tinymce_root/plugins/{advimage,advlink,example,fullpage,style,simple}

echo "*** Removing unneeded skins ..."
rm -rf $tinymce_root/themes/advanced/skins/{default,highcontrast,o2k7}

# plugins modifications
find $tinymce_root -name '*.html' -not -regex '.*/AtD/.*' -execdir mv "{}" "{}.pt" \;
find $tinymce_root -name '*.htm' -execdir mv "{}" "{}.pt" \;

find $tinymce_root -name "*_src.js" -delete

echo "*** Updating language files ..."
cd $product_root/utils/
if [ ! -d $product_root/utils/xml ]
then
    echo "*** Fetching translations ... ***"
    python wget-xml.py
    wget "http://www.tinymce.com/i18n/index.php?ctrl=export&act=zip" -O $root/tinymce_language_pack.zip --post-data="la%5B%5D=sq&la%5B%5D=ar&la%5B%5D=hy&la%5B%5D=az&la%5B%5D=eu&la%5B%5D=be&la%5B%5D=bn&la%5B%5D=nb&la%5B%5D=bs&la%5B%5D=br&la%5B%5D=bg&la%5B%5D=my&la%5B%5D=ca&la%5B%5D=km&la%5B%5D=ch&la%5B%5D=zh&la%5B%5D=hr&la%5B%5D=cs&la%5B%5D=da&la%5B%5D=dv&la%5B%5D=nl&la%5B%5D=en&la%5B%5D=eo&la%5B%5D=et&la%5B%5D=fi&la%5B%5D=fr&la%5B%5D=qc&la%5B%5D=gl&la%5B%5D=ka&la%5B%5D=de&la%5B%5D=el&la%5B%5D=gu&la%5B%5D=he&la%5B%5D=hi&la%5B%5D=hu&la%5B%5D=is&la%5B%5D=id&la%5B%5D=ia&la%5B%5D=it&la%5B%5D=ja&la%5B%5D=kl&la%5B%5D=ko&la%5B%5D=lv&la%5B%5D=lt&la%5B%5D=lb&la%5B%5D=mk&la%5B%5D=ms&la%5B%5D=ml&la%5B%5D=mn&la%5B%5D=se&la%5B%5D=no&la%5B%5D=nn&la%5B%5D=fa&la%5B%5D=pl&la%5B%5D=pt&la%5B%5D=ps&la%5B%5D=ro&la%5B%5D=ru&la%5B%5D=sc&la%5B%5D=sr&la%5B%5D=cn&la%5B%5D=si&la%5B%5D=sk&la%5B%5D=sl&la%5B%5D=es&la%5B%5D=sv&la%5B%5D=ta&la%5B%5D=tt&la%5B%5D=te&la%5B%5D=th&la%5B%5D=tn&la%5B%5D=tr&la%5B%5D=tw&la%5B%5D=uk&la%5B%5D=ur&la%5B%5D=vi&la%5B%5D=cy&la%5B%5D=zu&la%5B%5D=zh-tw&la%5B%5D=zh-cn&la_export=js&pr_id=7&submitted=Download"
    unzip $root/tinymce_language_pack.zip -d $root
    cp -R $root/tinymce_language_pack/langs/* $tinymce_root/langs/
    cp -R $root/tinymce_language_pack/themes/advanced/langs/* $tinymce_root/themes/advanced/langs/
    for f in $root/tinymce_language_pack/plugins/*
    do
        plugin_dest=$tinymce_root/plugins/`basename $f`
        if [ -d $plugin_dest ]
        then
            cp -R $f/langs/* $plugin_dest/langs/
        fi
    done
    # some files have wrong encoding
    sed -i 's/encoding=".*"/encoding="utf-8"/' xml/*

    python generate-po.py
    python compile-mo.py
    rm $root/tinymce_language_pack.zip
else
    echo "*** Translations already there, copy them over ***"
    # we erase translations on each update, so we have to copy them to tinymce source
    cp -R $root/tinymce_language_pack/langs/* $tinymce_root/langs/
    cp -R $root/tinymce_language_pack/themes/advanced/langs/* $tinymce_root/themes/advanced/langs/
    for f in $root/tinymce_language_pack/plugins/*
    do
        plugin_dest=$tinymce_root/plugins/`basename $f`
        if [ -d $plugin_dest ]
        then
            cp -R $f/langs/* $plugin_dest/langs/
        fi
    done
fi
cd $root

echo "*** Done. Don't forget to update CHANGELOG and commit!"
