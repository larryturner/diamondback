""" **Description**

        State interface.

    **Example**

        ::

            from diamondback.commons.Serial import Serial
            from diamondback.interfaces.IState import IState

            class Test( IState ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.state = ''

            test = Test( )

            test.state = Serial.encode( { 'a' : 0.0, 'b' : 1.0 } )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-07-12.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual


class IState( IEqual ) :

    """ State interface.
    """

    @property
    def state( self ) :

        """ State ( any ).
        """

        return self._state

    @state.setter
    def state( self, state : any ) :

        self._state = state

    def __eq__( self, other : any ) -> bool :

        """ Equality.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.state == other.state ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._state = [ ]
