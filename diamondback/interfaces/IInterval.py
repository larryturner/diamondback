""" **Description**

        Interval interface.

    **Example**

        ::

            from diamondback.interfaces.IInterval import IInterval


            class Test( IInterval ) :

                def __init__( self ) :

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
    def interval( self, interval ) :

        if ( interval < 0.0 ) :

            raise ValueError( 'Interval = ' + str( interval ) )

        self._interval = interval

    def __eq__( self, other ) :

        """ Evaluates equality condition.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.isclose( self.interval, other.interval ) ) )

    def __init__( self ) :

        """ Initializes an instance.
        """

        super( ).__init__( )

        self._interval = 0.0
