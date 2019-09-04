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

    with open( "readme.md", "r" ) as fin :

        _readme = fin.read( )

except :

    _readme = ''


setup( name = 'diamondback',
       version = diamondback.__version__,
       author = 'Larry Turner',
       author_email = 'larry.turner@se.com',
       url = 'https://github.com/larryturner/diamondback',
       description = 'Diamondback DSP package including commons, filters, interfaces, models, and transforms.',
       long_description = _readme,
       classifiers = [ 'Operating System :: OS Independent',
                       'Programing Language :: Python :: 3',
                       '**License** :: OSI Approved :: BSD-3C License' ],
       install_requires = [ 'jsonpickle >= 1.2',
                            'numpy >= 1.0.0',
                            'scipy >= 1.0.0' ],
       keywords = [ 'DSP',
                    'commons',
                    'filters',
                    'interfaces',
                    'models',
                    'transforms' ],
       packages = find_packages( ),
       license = 'BSD-3C.  Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.' )


