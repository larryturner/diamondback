""" **Description**

        Asset interface.

    **Example**

        ::

            from diamondback import IAsset
            import uuid


            class Test( IAsset ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.asset = str( uuid.uuid4( ) )

            test = Test( )

            test.asset = '<Country-Region-City-Corporation-Site>-' + test.asset

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2021, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2021-02-01.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual


class IAsset( IEqual ) :

    """ Asset interface.
    """

    @property
    def asset( self ) :

        """ Asset ( any ).
        """

        return self._asset

    @asset.setter
    def asset( self, asset : any ) :

        self._asset = asset

    def __eq__( self, other : any ) -> bool :

        """ Equal.

            Arguments :

                other - Other ( any ).

            Returns :

                equality - Equality ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.asset == other.asset ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._asset = [ ]
