""" **Description**

        Period interface.

    **Example**

        ::

            from diamondback import IPeriod


            class Test( IPeriod ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.period = 0.0

            test = Test( )

            test.period = 300.0

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-07-12.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import numpy


class IPeriod( IEqual ) :

    """ Period interface.
    """

    @property
    def period( self ) :

        """ Period in seconds ( float ).
        """

        return self._period

    @period.setter
    def period( self, period : float ) :

        if ( period < 0.0 ) :

            raise ValueError( f'Period = {period}' )

        self._period = period

    def __eq__( self, other : any ) -> bool :

        """ Equal.

            Arguments :

                other - Other ( any ).

            Returns :

                equality - Equality ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.isclose( self.period, other.period ) ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._period = 0.0
