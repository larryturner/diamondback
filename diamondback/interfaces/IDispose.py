""" **Description**

        Dispose interface.

    **Example**

        ::

            from diamondback import IDispose


            class Test( IDispose ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.dispose = False

            test = Test( )

            test.dispose = True

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2020, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-10-22.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual


class IDispose( IEqual ) :

    """ Dispose interface.
    """

    @property
    def dispose( self ) :

        """ Dispose ( any ).
        """

        return self._dispose

    @dispose.setter
    def dispose( self, dispose : any ) :

        self._dispose = dispose

    def __eq__( self, other : any ) -> bool :

        """ Equality.

            Arguments :

                other - Other ( any ).

            Returns :

                equality - Equality ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.dispose == other.dispose ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._dispose = [ ]
