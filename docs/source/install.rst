Installation
============

Latest version
--------------

- Add Products.TinyMCE in your buildout.cfg to the eggs attributes
- Run buildout and (re)start Zope
- Use the quick installer to (re)install the product

For basic installation use the following section in your buildout::

    [buildout]
    ...
    eggs =
        ...
        Products.TinyMCE

Upgrading
*********

When you upgrade Products.TinyMCE you need to run 
the upgrade steps in portal_setup in ZMI.

* Go to ZMI
* Go to portal_setup
* Choose *Upgrades* tab
* Run upgrade steps for Products.TinyMCE


Development version
-------------------

Please refer to :ref:`development-manual`, it is really important to read and understand the whole section.
