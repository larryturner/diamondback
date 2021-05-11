""" **Description**

        Diamondback setup.

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-23.

    **Definition**

"""

from diamondback.__metadata__ import __version__
from setuptools import find_packages, setup


try :

    with open( 'readme.rst', 'r' ) as fin :

        x = fin.read( )

        description = x[ x.index( 'Diamondback' ) : x.index( 'Details' ) ]

except Exception :

    description = ''


setup( name = 'diamondback',
       version = __version__,
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
       install_requires = [ 'jsonpickle >= 2.0.0',
                            'loguru >= 0.5.3',
                            'numpy >= 1.20.2',
                            'pandas >= 1.2.4',
                            'requests >= 2.25.1',
                            'scipy >= 1.6.3' ],
       extras_require = { 'full' : [ 'ipython >= 7.22.0',
                                     'ipywidgets >= 7.6.3',
                                     'jupyter >= 1.0.0',
                                     'matplotlib >= 3.4.1',
                                     'nox >= 2020.12.31',
                                     'pillow >= 8.2.0',
                                     'pytest >= 6.2.3',
                                     'regex >= 2021.4.4',
                                     'setuptools >= 56.0.0',
                                     'sphinx >= 3.5.4',
                                     'sphinx-pydantic >= 0.1.1',
                                     'sphinx-rtd-theme >= 0.5.2' ] },
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


