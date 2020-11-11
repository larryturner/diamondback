""" **Description**

        Sphinx document builder configuration.

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-03-22.

    **Definition**
    
"""

import os
import sphinx_rtd_theme
import sys


# -- Path --------------------------------------------------------------------

sys.path.insert( 0, os.path.abspath( '../' ) )

# -- Project -----------------------------------------------------------------

author = 'Larry Turner'

copyright = '2018, Larry Turner, Schneider Electric'

project = 'diamondback'

# -- Configuration -----------------------------------------------------------

exclude_patterns = [ 'build' ]

extensions = [ 'sphinx.ext.autodoc',
               'sphinx.ext.githubpages',
               'sphinx.ext.napoleon',
               'sphinx.ext.viewcode',
               'sphinx-pydantic' ]

pygments_style = 'friendly'

templates_path = [ 'templates' ]

# -- Extensions --------------------------------------------------------------

autoclass_content = 'both'

autodoc_default_options = { 'members' : True }

autodoc_member_order = 'bysource'

napoleon_google_docstring = True

napoleon_include_init_with_doc = False

napoleon_include_private_with_doc = False

napoleon_include_special_with_doc = False

# -- Theme--------------------------------------------------------------------

html_theme = 'sphinx_rtd_theme'

html_theme_path = [ sphinx_rtd_theme.get_html_theme_path( ) ]

# -- Help --------------------------------------------------------------------

htmlhelp_basename = project + 'doc'
