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
    'ar bs ch da el es fa fr he hu ii it lv ms nl pl ro sc si sl sr '
    'tr tw vi bg ca cs de en et eu fi gl hr ia is ja lt mk nb nn pt ru se '
    'sk sq sv tt uk'.split())

def main():

    if not os.path.exists('xml'):
        os.mkdir('xml')

    for x in AVAILABLE_LANGUAGES:

        cmd = __WGET + (' -O xml/%s.xml "http://services.moxiecode.com/i18n/download.aspx?format=xml&code=%s&product=tinymce"') % (x, x)
        os.system(cmd)

if __name__ == '__main__':
    main()
