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

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-01-09.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import os

class IPath( IEqual ) :

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

    def __eq__( self, other : any ) -> bool :

        """ Equal.

            Arguments :

                other : any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( self.path == other.path ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._path = None
