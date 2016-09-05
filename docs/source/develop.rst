.. _developer-manual:

Developing TinyMCE
^^^^^^^^^^^^^^^^^^

Prerequisites
-------------

If you are on a Mac, install `apache-ant` from macports. Otherwise:

- Install the Java JDK or JRE packages
- Install Apache Ant
- Add Apache Ant to your systems path environment variable. This is not
  required but makes it easier to issue commands to Ant without having to type
  the full path for it.


First start
-----------

TinyMCE integration in Plone has two core packages:

* `Products.TinyMCE`: Plone integration
* `tinymce`: raw tinymce source files

Fork both packages: https://github.com/plone/Products.TinyMCE and
https://github.com/collective/tinymce. Continue with cloning your fork
of ``Products.TinyMCE`` to your local machine::

    $ git clone git@github.com:<your_git_username>/Products.TinyMCE.git
    $ cd Products.TinyMCE

Now you need to tell buildout to use your fork of ``tinymce``. Do that by
opening up ``buildout.cfg`` with your favorite editor and changing the
``tinymce = ...`` line in ``[sources]`` section so it points to your fork::

    - tinymce = git https://github.com/collective/tinymce.git egg=false branch=3.4.7-plone
    + tinymce = git https://github.com/<your_git_username>/tinymce.git egg=false branch=3.4.7-plone

Cool, you are now ready to build your development environment::

    $ python2.6 bootstrap.py
    $ bin/buildout

What follows is going into src/tinymce, running a script to build TinyMCE
and copy them in `skin` directory where Plone can use them. To do so run::

    $ ./upgrade_tinymce.sh

Ok, ready to start Zope and apply upgrade steps to your site. Once started go to
http://localhost:8080/Plone/portal_setup/manage_upgrades and choose
``Products.TinyMCE:TinyMCE`` as a profile. If upgrades are available, run them.
If you see ``No upgrade avaiable`` you don't need to run anything.

# TODO: difference using development version and developing tinymce

Upgrading
-----------

When you upgrade Products.TinyMCE you need to run
the upgrade steps in portal_setup in ZMI.

* Go to /Plone/portal_setup/manage_upgrades
* Run upgrade steps for Products.TinyMCE


After each change
-----------------

If you change something in *src/tinymce* you need to rerun the tinymce builder script and
restart Plone

    $ ./upgrade_tinymce.sh
    $ bin/instance fg


.. warning::

    Never change files directly in skins, but rather in src/tinymce/

Debugging tinymce javascript
----------------------------

You can have unobfuscated TinyMCE available for your Plone for debugging in two ways

* Separate files: TinyMCE uses internal script loader

* Merged as tiny_mce_full.js

The former is recommended.

Development build
=========================

All TinyMCE source code modules are separate in the orignal tree and must be copied for to *skins* structure::

        cd src/tinymce/jscripts/tiny_mce
        cp -r * ../../../../Products/TinyMCE/skins/tinymce

In *portal_javascripts* change *tiny_mce.js* -> *tiny_mce_dev.js*.

Fix definitionlist: in *skins/tinymce/plugins/definitionlist* copy *editor_plug.js* as *editor_plugin_src.js*.
Don't know why this thing is broken or what's the proper fix or why Sky is blue.

Uncompressed jQuery adapter must be manually installed too.
From *skins/classes/adapter/jquery* copy *adapter.js* as *skins/jquery.tinymce.js*.

Full concatenated build
=========================

Edit ``upgrade_tinymce.sh`` to do a full build::

        ant -s $tinymce_git_root/build.xml build_full

This will create *skins/tinymce/tiny_mce_full.js*.

Copy in jquery.tinymce.js (where?)

More info about TinyMCE build process:

* https://github.com/tinymce/tinymce

Updating translations
---------------------

We use two domains of translations:

 * tinymce.po files which contain TinyMCE core translations and which are only
   updated when we upgrade to a new version of TinyMCE (see below) - no touchy!
 * plone.tinymce.po files which contain translations for our custom code.

Before editing translations

* install ``i18ndude`` by running buildout using instructions above.

* make sure your OS has ``msgfmt`` command installed

If you change some of our templates or control panels, make sure you rebuild our
plone.tinymce.pot file and re-sync all language files::

   export BIN=`pwd`/bin
   cd Products/TinyMCE/locales
   $BIN/i18ndude rebuild-pot --exclude "utils support" --pot plone.tinymce.pot --merge plone.tinymce-manual.pot --create plone.tinymce ../
   $BIN/i18ndude sync --pot plone.tinymce.pot ./*/LC_MESSAGES/plone.tinymce.po

.. note ::

        Exclude list is based on HTML files which Zope TAL interpreter cannot scan properly:
        it gives NestingErrors becase it tries to scan HTML tags inside Javascript strings.
        You may need update this list based on TinyMCE release.

After this (or if you only change a translation string itself), you need to
recompile .mo files::

    cd Products/TinyMCE/locales/<your_language>/LC_MESSAGES
    msgfmt -o plone.tinymce.mo plone.tinymce.po

Update language files for TinyMCE core
--------------------------------------

Whenever we upgrade to a new version of TinyMCE, we also need to fetch
the latest language files for TinyMCE core and convert them to .po files,
that Plone can use. You do that by using the scripts in
``Products/TinyMCE/utils``::

    # download XML language files
    $ cd Products/TinyMCE/utils
    $ python wget-xml.py

    # convert downloaded xml files into .po files
    $ python generate-po.py

    # compile .mo files out of .po files
    $ python compile-po.py

    # create tinymce.pot which is needed for pobuddy.py support
    $ cp ../locales/en/LC_MESSAGES/tinymce.po ../locales/tinymce.pot

Compile translation files
-------------------------

A one-liner to compile all translation files goes a little something like this::

    $ cd Products/TinyMCE/locales
    $ for po in `find . -name "*.po"` ; do msgfmt -o `dirname $po`/`basename $po .po`.mo $po; done

Translating style names
=======================

TODO: How????

Common pitfalls
---------------

If your TinyMCE is not working as excpected or is not displayed at all,
first check you haven't fallen in one of the following pits.

Building TinyMCE failed
=======================

Maybe the ``upgrade_tinymce.sh`` script failed halfway through its
process. Stop Zope and rerun the script until you see an output like this::

    ...
    BUILD SUCCESSFUL
    Total time: 4 seconds
    *** Cleaning old tinymce version ...
    *** Copying files ...
    *** Removing unneeded files ...
    *** Removing unneeded plugins ...
    *** Removing unneeded skins ...
    *** Updating language files ...
    *** Translations already there, copy them over ***

Use correct tinymce branch
==========================

Go to ``src/tinymce/`` and make sure you are using the latest plone branch
of TinyMCE. The output should look something like this, with ``*`` indicating
which branch you are on::

    $ git branch
    * 3.4.3-plone
      master


Getting a new upstream version
------------------------------

Let's say current version in Products.TinyMCE is 3.4.3 and upstream is 3.4.7::

    $ cd src/tinymce
    $ git checkout 3.4.3
    $ git checkout -b 3.4.7
    $ git rebase --ignore-whitespace --onto 3.4.7-plone 3.4.3 3.4.7

Ignore whitespace makes sure different lineendings are not an issue while merging.

PS: It is highly recommended to use meld for merging::

    $ git config --global merge.tool meld


Releasing TinyMCE
-----------------

* run ./upgrade_tinymce.sh
* rebuild pot and sync (look above)
* compile translation files (look above)
* commit all changes in skins directory with message like "sync with tinymce at revision x"
* increment version in setup.py
* run python setup.py sdist


Javascript coding standards
---------------------------

use jslint, if you don't have it integrated with editor yet, use http://www.jslint.com/
