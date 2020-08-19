""" **Description**

        Setup.

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

    with open( 'readme.md', 'r' ) as fin :

        _readme = fin.read( )

except :

    _readme = ''


setup( name = 'diamondback',
       version = diamondback.__version__,
       author = 'Larry Turner',
       author_email = 'larry.turner@se.com',
       url = 'https://github.com/larryturner/diamondback',
       description = 'Diamondback Digital Signal Processing ( DSP ) package including commons, filters, interfaces, models, and transforms.',
       long_description = _readme,
       classifiers = [ 'Operating System :: OS Independent',
                       'Programming Language :: Python :: 3',
                       'License :: OSI Approved :: BSD License' ],
       install_requires = [ 'jsonpickle >= 1.4.1',
                            'numpy >= 1.19.1',
                            'scipy >= 1.5.2' ],
       keywords = [ 'DSP',
                    'FFT',
                    'FIR',
                    'GZIP',
                    'IIR',
                    'JSON',
                    'PCA',
                    'PID',
                    'PSD',
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
                    'serial',
                    'transform',
                    'wavelet' ],
       packages = find_packages( ),
       python_requires = '>= 3.5',
       license = 'BSD-3C.  Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.' )


