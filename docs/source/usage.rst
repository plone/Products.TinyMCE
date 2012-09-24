Usage
=====

Enable After the Deadline spelling and grammar checker
------------------------------------------------------

- Go to the Plone control panel and click on "TinyMCE Visual Editor"
- Click on 'Toolbar' (middle left)
- Make sure that 'spellchecker' is checked.
- Click on 'Libraries' (top right)
- Under "Spellchecker plugin to use", choose 'After the deadline'
- Under AtD Service URL, choose your ATD server's URL. (The default is their
  public service)
- It's however recommended that you install your own ATD spellchecker service 
  See here for more details: http://open.afterthedeadline.com/how-to/get-started/

You should now have AtD enabled and have a spellcheck button in TinyMCE.

Widget configuration
----------------------

You can configure TinyMCE per-widget level for different fields.

`TinyMCE's utility.getConfiguration() looks for a widget specific configuration <https://github.com/plone/Products.TinyMCE/blob/master/Products/TinyMCE/utility.py#L719>_`.
The options below are provided. Please check the source code of ``getConfiguration()`` 
above for the full list.

* filter_buttons
* allow_buttons 
* redefine_parastyles
* parastyles 
* rooted
* toolbar_width

Here is an example how to configure field specific TinyMCE button list with reduced
formatting options::

    atapi.TextField(
        'text',
        allowable_content_types=('text/html',),
        default_output_type='text/html',
        widget=atapi.RichWidget(
            label=_(u"Long description"),
            description=_(u"Long descriiption about the product with links to the further information"),
            allow_buttons=(
                    'pasteword',
                    'bg-basicmarkup',
                    'bold-button',
                    'italic-button',
                    'bg-drawers',
                    'linklibdrawer-button',
                    'linkdrawer-button',
                    'removelink-button',
                    'source',
                    'list-ul-addbutton',
            ),
        ),
    ),


