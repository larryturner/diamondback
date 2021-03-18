""" **Description**

        Interval interface.

    **Example**

        ::

            from diamondback import IInterval


            class Test( IInterval ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.interval = 0.0

            test = Test( )

            test.interval = 7200.0

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-07-12.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import numpy


class IInterval( IEqual ) :

    """ Interval interface.
    """

    @property
    def interval( self ) :

        """ Interval in seconds ( float ).
        """

        return self._interval

    @interval.setter
    def interval( self, interval : float ) :

        if ( interval < 0.0 ) :

            raise ValueError( f'Interval = {interval}' )

        self._interval = interval

    def __eq__( self, other : any ) -> bool :

        """ Equal.

            Arguments :

                other - Other ( any ).

            Returns :

                equality - Equality ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.isclose( self.interval, other.interval ) ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._interval = 0.0
