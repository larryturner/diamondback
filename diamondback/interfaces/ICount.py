""" **Description**

        Count interface.

    **Example**

        ::

            from diamondback import ICount


            class Test( ICount ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.count = 0

            test = Test( )

            test.count = 3

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2021, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2021-01-08.

    **Definition**
"""

from diamondback.interfaces.IEqual import IEqual


class ICount( IEqual ) :

    """ Count interface.
    """

    @property
    def count( self ) :

        """ Count ( int ).
        """

        return self._count

    @count.setter
    def count( self, count : int ) :

        if ( count < 0 ) :

            raise ValueError( 'Count = ' + str( count ) )

        self._count = count

    def __eq__( self, other : any ) -> bool :

        """ Equality.

            Arguments :

                other - Other ( any ).

            Returns :

                equality - Equality ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.count == other.count ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._count = 0
