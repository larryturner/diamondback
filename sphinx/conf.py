""" **Description**

        Diamondback sphinx documentation configuration.

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-03-22.

    **Definition**

"""

import os
import sys


# Path.

sys.path.insert( 0, os.path.abspath( '../' ) )

# Project.

author = 'Larry Turner'

copyright = '© 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.'

project = 'diamondback'

# Configuration.

exclude_patterns = [ 'build', 'modules.rst', 'noxfile.rst', 'setup.rst' ]

extensions = [ 'sphinx.ext.autodoc',
               'sphinx.ext.autosummary',
               'sphinx.ext.githubpages',
               'sphinx.ext.intersphinx',
               'sphinx.ext.napoleon',
               'sphinx.ext.viewcode',
               'sphinx-pydantic' ]

templates_path = [ 'templates' ]

# Extensions.

autoclass_content = 'both'

autodoc_default_options = { 'members' : True }

autodoc_member_order = 'bysource'

autosummary_generate = True

intersphinx_mapping = { 'python' : ( 'https://docs.python.org/3', None ),
                        'pandas' : ( 'https://pandas.pydata.org/docs/', None ),
                        'numpy' : ( 'https://docs.scipy.org/doc/numpy/', None ),
                        'plotly' : ( 'https://plotly.com/python-api-reference/', None ) }

napoleon_google_docstring = True

napoleon_include_init_with_doc = False

napoleon_include_private_with_doc = True

napoleon_include_special_with_doc = True

napolean_use_admonition_for_examples = True

napolean_use_admonition_for_notes = True

napolean_use_rtype = False

# Theme.

html_theme = 'sphinx_rtd_theme'

# Help.

htmlhelp_basename = project + 'doc'
