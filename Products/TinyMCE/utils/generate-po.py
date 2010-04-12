#!/opt/local/bin/python2.4

import os

try:
    from xml.etree import ElementTree as ET
except ImportError:
    from elementtree import ElementTree as ET

AVAILABLE_LANGUAGES = set(
    'sq ar hy az eu be bn nb bs br bg ca ch zh hr cs da dv nl en et fi fr gl '
    'de el gu he hi hu is id ia it ja ko lv lt lb mk ms ml mn se no nn fa pl '
    'pt ps ro ru sc sr ii si sk sl es sv ta tt te th tr tw uk ur cy vi zu'.split())

for x in AVAILABLE_LANGUAGES:
    print "Parsing xml/%s.xml" % (x)
    tree = ET.parse("xml/%s.xml" % (x))

    root = tree.getroot()
    header = root.find('header')
    author = header.find('author').text.encode("utf-8")
    version = header.find('version')
    version_major = version.attrib['major']
    version_minor = version.attrib['minor']
    version_releasedate = version.attrib['releasedate']
    description = header.find('description').text
    description = description.replace('\n', '\\n')
    description = description.encode("utf-8")

    language = root.find('language')
    title = language.attrib['title'].encode("utf-8")
    dir = language.attrib['dir']

    if not os.path.exists("../locales/%s" % x):
        os.mkdir("../locales/%s" % x)

    if not os.path.exists("../locales/%s/LC_MESSAGES" % x):
        os.mkdir("../locales/%s/LC_MESSAGES" % x)

    FILE = open("../locales/%s/LC_MESSAGES/tinymce.po" % (x), "w")

    FILE.write("# %s\n" % description)
    FILE.write("# Version %s.%s\n" % (version_major, version_minor))
    FILE.write("#\n")
    FILE.write("# %s\n" % author)
    FILE.write("msgid \"\"\n")
    FILE.write("msgstr \"\"\n")
    FILE.write("\"Project-Id-Version: Products.TinyMCE\\n\"\n")
    FILE.write("\"POT-Creation-Date: 2000-01-01 00:00+0000\\n\"\n")
    FILE.write("\"PO-Revision-Date: %s 00:00+0000\\n\"\n" % version_releasedate)
    FILE.write("\"Last-Translator: %s\\n\"\n" % author)
    FILE.write("\"Language-Team: %s\\n\"\n" % author)
    FILE.write("\"MIME-Version: 1.0\\n\"\n")
    FILE.write("\"Content-Type: text/plain; charset=UTF-8\\n\"\n")
    FILE.write("\"Content-Transfer-Encoding: 8bit\\n\"\n")
    FILE.write("\"Plural-Forms: nplurals=1; plural=0;\\n\"\n")
    FILE.write("\"Language-Code: %s\\n\"\n" % x)
    FILE.write("\"Language-Name: %s\\n\"\n" % title)
    FILE.write("\"Preferred-Encodings: utf-8 latin1\\n\"\n")
    FILE.write("\"Domain: tinymce\\n\"\n")
    FILE.write("\n")

    for group in language.getiterator('group'):
        for item in group.getiterator('item'):
            domain = group.attrib['target']
            if domain == 'advlink':
                domain = 'plonelink'
            if domain == 'advimage':
                domain = 'ploneimage'
            if domain == 'advlink_dlg':
                domain = 'plonelink_dlg'
            if domain == 'advimage_dlg':
                domain = 'ploneimage_dlg'
            FILE.write("msgid \"%s_%s\"\n" % (domain,item.attrib['name']))
            if item.text:
                msg = item.text.replace('"', '\\"')
                msg = msg.replace('\\N', '\\n')
                msg = msg.replace('\n', '\\n')
                msg = msg.replace('\\\'', '\'')
                if msg.startswith('\\n'):
                    msg = msg[2:]
                FILE.write("msgstr \"%s\"\n" % msg.encode("utf=8"))
            else:
                FILE.write("msgstr \"\"\n")
            FILE.write("\n")

    FILE.close()
