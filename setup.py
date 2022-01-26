""" **Description**
        Diamondback setup.

    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2022 Larry Turner, Schneider Electric Industries SAS. All rights reserved.
    
    **Author**
        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-23.
"""

from setuptools import find_packages, setup
import os
import re

try :
    with open( 'readme.rst', 'r' ) as fin :
        description = fin.read( )
except Exception :
    description = ''
name = 'diamondback'
with open( name + os.path.sep + '__init__.py', 'r' ) as fin :
    label, value = r'__version__\s{0,4}=\s{0,4}', r'\d{1,3}\.\d{1,3}\.\d{1,3}'
    version = re.findall( value, re.findall( label + '\W' + value + '\W', fin.read( ) )[ 0 ] )[ 0 ]
setup( name = name,
       version = version,
       author = 'Larry Turner',
       author_email = 'larry.turner@se.com',
       url = 'https://github.com/larryturner/diamondback',
       description = 'Diamondback digital signal processing package.',
       long_description = description,
       classifiers = [ 'Operating System :: OS Independent',
                       'Programming Language :: Python :: 3',
                       'Programming Language :: Python :: 3.6',
                       'Programming Language :: Python :: 3.7',
                       'Programming Language :: Python :: 3.8',
                       'Programming Language :: Python :: 3.9',
                       'Programming Language :: Python :: 3.10',
                       'License :: OSI Approved :: BSD License' ],
       install_requires = [ 'jsonpickle >= 2.0.0, < 3.0.0',
                            'loguru >= 0.5.3, < 1.0.0',
                            'numpy >= 1.21.4, < 2.0.0',
                            'pandas >= 1.3.4, < 2.0.0',
                            'requests >= 2.26.0, < 3.0.0',
                            'scipy >= 1.7.2, < 2.0.0' ],
       extras_require = dict( full = [ 'ipython >= 7.29.0, < 8.0.0',
                                       'ipywidgets >= 7.6.5, < 8.0.0',
                                       'jupyter >= 1.0.0, < 2.0.0',
                                       'matplotlib >= 3.5.0, < 4.0.0',
                                       'nox >= 2021.10.1, < 2023.10.1',
                                       'pillow >= 9.0.0, < 10.0.0',
                                       'pytest >= 6.2.5, < 7.0.0',
                                       'setuptools >= 59.2.0, < 60.0.0',
                                       'sphinx >= 4.3.0, < 5.0.0',
                                       'sphinx-rtd-theme >= 1.0.0, < 2.0.0' ] ),
       keywords = [ 'BSON',
                    'DSP',
                    'FFT',
                    'FIR',
                    'GZIP',
                    'IIR',
                    'JSON',
                    'PCA',
                    'PID',
                    'PSD',
                    'REST',
                    'adaptive',
                    'complex',
                    'derivative',
                    'diamondback',
                    'diversity',
                    'exponential',
                    'filter',
                    'fourier',
                    'frequency',
                    'goertzel',
                    'integral',
                    'jsonpickle',
                    'log',
                    'loguru',
                    'model',
                    'polynomial',
                    'polyphase',
                    'power',
                    'rate',
                    'requests',
                    'serial',
                    'transform',
                    'wavelet' ],
       packages = find_packages( exclude = [ 'tests', 'tests.*' ] ),
       python_requires = '>= 3.6',
       license = 'BSD-3C.  © 2018 - 2022 Larry Turner, Schneider Electric Industries SAS. All rights reserved.' )


