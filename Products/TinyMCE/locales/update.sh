i18ndude rebuild-pot --pot plone.tinymce.pot --merge plone.tinymce-manual.pot --create plone.tinymce ../
i18ndude sync --pot plone.tinymce.pot ./*/LC_MESSAGES/plone.tinymce.po
