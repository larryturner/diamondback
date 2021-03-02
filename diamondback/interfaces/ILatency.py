""" **Description**

        Latency interface.

    **Example**

        ::

            from diamondback import ILatency


            class Test( ILatency ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.latency = 0.0

            test = Test( )

            test.latency = 600.0

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-07-12.

    **Definition**
"""

from diamondback.interfaces.IEqual import IEqual
import numpy


class ILatency( IEqual ) :

    """ Latency interface.
    """

    @property
    def latency( self ) :

        """ Latency in seconds ( float ).
        """

        return self._latency

    @latency.setter
    def latency( self, latency : float ) :

        if ( latency < 0.0 ) :

            raise ValueError( 'Latency = {}'.format( latency ) )

        self._latency = latency

    def __eq__( self, other : any ) -> bool :

        """ Equality.

            Arguments :

                other - Other ( any ).

            Returns :

                equality - Equality ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.isclose( self.latency, other.latency ) ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._latency = 0.0
