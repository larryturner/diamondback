""" **Description**
        Path interface.

    **Example**
       
        ::
        
            from diamondback import IPath

            class Test( IPath ) :

                def __init__( self ) -> None :
                    super( ).__init__( )
                    self.path = ''

            test = Test( )
            test.path = '.\data'

    **License**
        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, Analytics & AI, 2020-01-09.
"""

import os

class IPath( object ) :

    """ Path interface.
    """

    @property
    def path( self ) :

        """ path : str.
        """

        return self._path

    @path.setter
    def path( self, path : str ) :

        if ( path ) :
            path = path.replace( '/', os.path.sep ).replace( '\\', os.path.sep )
            if ( not os.path.exists( path ) ) :
                raise FileNotFoundError( f'Path = {path}' )
        self._path = path

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )
        self._path = ''
