""" **Description**

        Diamondback setup.

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-23.

    **Definition**

"""

from setuptools import find_packages, setup
import diamondback


try :

    with open( 'readme.rst', 'r' ) as fin :

        _readme = fin.read( )

except :

    _readme = ''


setup( name = 'diamondback',
       version = diamondback.__version__,
       author = 'Larry Turner',
       author_email = 'larry.turner@se.com',
       url = 'https://github.com/larryturner/diamondback',
       description = 'Diamondback digital signal processing package.',
       long_description = _readme,
       classifiers = [ 'Operating System :: OS Independent',
                       'Programming Language :: Python :: 3',
                       'License :: OSI Approved :: BSD License' ],
       install_requires = [ 'jsonpickle >= 2.0.0',
                            'numpy >= 1.20.1',
                            'pandas >= 1.2.2',
                            'python-dateutil >= 2.8.1',
                            'requests >= 2.25.1',
                            'scipy >= 1.6.0' ],
       keywords = [ 'DSP',
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
                    'diversity',
                    'exponential',
                    'filter',
                    'fourier',
                    'frequency',
                    'goertzel',
                    'integral',
                    'log',
                    'model',
                    'polynomial',
                    'polyphase',
                    'power',
                    'rate',
                    'serial',
                    'transform',
                    'wavelet' ],
       packages = find_packages( ),
       python_requires = '>= 3.7',
       license = 'BSD-3C.  Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.' )


