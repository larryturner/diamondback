""" **Description**

        Period interface.

    **Example**

        ::

            from diamondback.interfaces.IPeriod import IPeriod


            class Test( IPeriod ) :

                def __init__( self ) :

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
    def period( self, period ) :

        if ( period < 0.0 ) :

            raise ValueError( 'Period = ' + str( period ) )

        self._period = period

    def __eq__( self, other ) :

        """ Evaluates equality condition.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.isclose( self.period, other.period ) ) )

    def __init__( self ) :

        """ Initializes an instance.
        """

        super( ).__init__( )

        self._period = 0.0
