""" **Description**
        Sphinx documentation configuration.
    
    **License**
        © 2019 - 2022 Schneider Electric Industries SAS. All rights reserved.
    
    **Author**
        Larry Turner, Schneider Electric, AI Hub, 2019-03-22.
"""

import os
import sys

# Path.

sys.path.insert( 0, os.path.abspath( '..' ) )

# Project.

author = 'Larry Turner'
copyright = '© 2019 - 2022 Schneider Electric Industries SAS. All rights reserved.'
project = os.getcwd( ).split( os.path.sep )[ -2 ]
title = 'Diamondback DSP'

# Extensions.

extensions = [ 'sphinx.ext.autosummary',
               'sphinx.ext.githubpages',
               'sphinx.ext.intersphinx',
               'sphinx.ext.napoleon',
               'sphinx.ext.viewcode' ]

# Configuration.

autoclass_content = 'both'
autosummary_generate = True
autosummary_imported_members = True
autosummary_ignore_module_all = False
exclude_patterns = [ 'build', 'tests' ]
html_theme = 'sphinx_rtd_theme'
html_title = title
intersphinx_mapping = dict( numpy = ( 'https://numpy.org/doc/stable', None ),
                            pandas = ( 'https://pandas.pydata.org/docs', None ),
                            python = ( 'https://docs.python.org/3', None ),
                            request = ( 'https://requests.readthedocs.io/en/latest', None ),
                            sklearn = ( 'https://scikit-learn.org/stable', None ) )
master_doc = 'index'
napoleon_google_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napolean_use_admonition_for_examples = True
napolean_use_admonition_for_notes = True
napolean_use_rtype = False
