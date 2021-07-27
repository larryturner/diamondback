""" **Description**

        Diamondback setup.

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-23.

    **Definition**

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
                       'License :: OSI Approved :: BSD License' ],
       install_requires = [ 'jsonpickle >= 2.0.0, <= 3.0.0',
                            'loguru >= 0.5.3, <= 1.5.3',
                            'numpy >= 1.21.1, <= 2.21.1',
                            'pandas >= 1.3.1, <= 2.3.1',
                            'requests >= 2.26.0, <= 3.26.0',
                            'scipy >= 1.7.0, <= 2.7.0' ],
       extras_require = { 'full' : [ 'ipython >= 7.25.0, <= 8.25.0',
                                     'ipywidgets >= 7.6.3, <= 8.6.3',
                                     'jupyter >= 1.0.0, <= 2.0.0',
                                     'matplotlib >= 3.4.2, <= 4.4.2',
                                     'nox >= 2021.6.12, <= 2023.6.12',
                                     'pillow >= 8.3.1, <= 9.3.1',
                                     'pytest >= 6.2.4, <= 7.2.4',
                                     'setuptools >= 57.0.0, <= 58.0.0',
                                     'sphinx >= 4.0.2, <= 5.0.2',
                                     'sphinx-rtd-theme >= 0.5.2, <= 1.5.2' ] },
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
       license = 'BSD-3C.  © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.' )


