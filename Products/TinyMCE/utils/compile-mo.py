#!/opt/local/bin/python2.4

from elementtree import ElementTree as ET
import os, sys, string

# Skip .ko for now
AVAILABLE_LANGUAGES = set(
    'ar bs ch da el es fa fr he hu ii it lv ms nl pl ro sc si sl sr '
    'tr tw vi bg ca cs de en et fi gl hr ia is ja lt mk nb nn pt ru se '
    'sk sq sv tt uk'.split())

for x in AVAILABLE_LANGUAGES:

    cmd = "msgfmt -o ../locales/%s/LC_MESSAGES/tinymce.mo ../locales/%s/LC_MESSAGES/tinymce.po" % (x, x)
    os.system(cmd)
