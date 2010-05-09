"""
   Usage: wget-xml.py
"""

import os, sys, string

try:
    import win32api
    WIN32 = True
except ImportError:
    WIN32 = False

__WGET = os.environ.get('WGET', 'wget')

AVAILABLE_LANGUAGES = set(
    'sq ar hy az eu be bn nb bs br bg ca ch zh hr cs da dv nl en et fi fr gl '
    'ka de el gu he hi hu is id ia it ja ko lv lt lb mk ms ml mn se no nn fa '
    'pl pt ps ro ru sc sr ii si sk sl es sv ta tt te th tr tw uk ur cy vi zu'.split())

def main():

    if not os.path.exists('xml'):
        os.mkdir('xml')

    for x in AVAILABLE_LANGUAGES:

        cmd = __WGET + (' -O xml/%s.xml "http://services.moxiecode.com/i18n/download.aspx?format=xml&code=%s&product=tinymce"') % (x, x)
        os.system(cmd)

if __name__ == '__main__':
    main()
