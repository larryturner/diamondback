""" **Description**
        Sphinx documentation configuration.

    **License**
        © 2018 - 2024 Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, AI Hub, 2019-03-22.
"""

import pathlib

# Project.

author = 'Larry Turner'
with open( str( pathlib.Path( pathlib.Path.cwd( ).parent / 'license' ) ), 'r' ) as fin :
    copyright = fin.readline( )[ 1 : -2 ]
project = pathlib.Path.cwd( ).parent.name
title = 'Diamondback Digital Signal Processing (DSP)'

# Extensions.

extensions = [ 'sphinx.ext.autosummary',
               'sphinx.ext.githubpages',
               'sphinx.ext.napoleon',
               'sphinx.ext.viewcode' ]

# Configuration.

autoclass_content = 'both'
autosummary_generate = True
autosummary_imported_members = True
autosummary_ignore_module_all = False
exclude_patterns = [ 'build', 'tests' ]
html_theme = 'sphinx_rtd_theme'
html_theme_options = dict( style_nav_header_background = 'black' )
html_title = title
master_doc = 'index'
napoleon_google_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napolean_use_admonition_for_examples = True
napolean_use_admonition_for_notes = True
napolean_use_rtype = False
