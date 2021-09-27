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
"""

class ICount( object ) :

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

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )
        self._count = 0
