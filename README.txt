TinyMCE
=======

Adds support for TinyMCE, a platform independent web based Javascript HTML
WYSIWYG editor, to Plone.

Feedback
--------

Please send any changes, improvements, or suggestions regarding this Plone
product to `Four Digits <mailto:info@fourdigits.nl>`_

Requirements
------------

TinyMCE is tested on Plone 4 and 3, please submit any compatibility issues
you may encounter.

Upgrading
-----------

When you upgrade from Products.TinyMCE 1.2 to 1.3 you need to run 
the upgrade steps in portal_setup in ZMI.

* Go to ZMI

* Go to portal_setup

* Choose *Upgrades* tab

* Run upgrade steps for Products.TinyMCE

As the result, the old ``tiny_mce.js`` and other files should be replaced with ``tiny_mce_jquery.js`` 
and ``jquery.tinymce.js`` in the site Javascript registry.
