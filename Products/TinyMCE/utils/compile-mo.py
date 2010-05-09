#!/opt/local/bin/python2.4

import os

try:
    from xml.etree import ElementTree as ET
except ImportError:
    from elementtree import ElementTree as ET

AVAILABLE_LANGUAGES = set(
    'sq ar hy az eu be bn nb bs br bg ca ch zh hr cs da dv nl en et fi fr gl '
    'ka de el gu he hi hu is id ia it ja ko lv lt lb mk ms ml mn se no nn fa '
    'pl pt ps ro ru sc sr ii si sk sl es sv ta tt te th tr tw uk ur cy vi zu'.split())

for x in AVAILABLE_LANGUAGES:

    cmd = "msgfmt -o ../locales/%s/LC_MESSAGES/tinymce.mo ../locales/%s/LC_MESSAGES/tinymce.po" % (x, x)
    os.system(cmd)
