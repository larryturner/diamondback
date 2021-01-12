""" **Description**

        Live interface.

    **Example**

        ::

            from diamondback import ILive


            class Test( ILive ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.live = False

            test = Test( )

            test.live = True

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2021, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2021-01-12.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual


class ILive( IEqual ) :

    """ Live interface.
    """

    @property
    def live( self ) :

        """ Live ( any ).
        """

        return self._live

    @live.setter
    def live( self, live : any ) :

        self._live = live

    def __eq__( self, other : any ) -> bool :

        """ Equality.

            Arguments :

                other - Other ( any ).

            Returns :

                equality - Equality ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.live == other.live ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._live = [ ]
