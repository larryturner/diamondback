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

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2021-01-08.

    **Definition**
"""

from diamondback.interfaces.IEqual import IEqual
import typing


class ICount( IEqual ) :

    """ Count interface.
    """

    @property
    def count( self ) :

        """ count : int - in [ 0, inf ).
        """

        return self._count

    @count.setter
    def count( self, count : int ) :

        if ( count < 0 ) :

            raise ValueError( f'Count = {count}' )

        self._count = count

    def __eq__( self, other : typing.Any ) -> bool :

        """ Equal.

            Arguments :

                other : typing.Any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( self.count == other.count ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._count = 0
