""" **Description**

        Path interface.

    **Example**

        ::

            from diamondback.interfaces.IPath import IPath

            class Test( IPath ) :

                def __init__( self ) :

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

        """ Path ( str ).
        """

        return self._path

    @path.setter
    def path( self, path ) :

        if ( path ) :

            path = path.replace( '/', os.path.sep ).replace( '\\', os.path.sep )

            if ( not os.path.exists( path ) ) :

                raise FileNotFoundError( 'Path = ' + str( path ) )

        self._path = path

    def __eq__( self, other ) :

        """ Evaluates equality condition.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.path == other.path ) )

    def __init__( self ) :

        """ Initializes an instance.
        """

        super( ).__init__( )

        self._path = [ ]