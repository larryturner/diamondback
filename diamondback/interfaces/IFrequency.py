""" **Description**

        Frequency interface.

    **Example**

        ::

            from diamondback import IFrequency


            class Test( IFrequency ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.frequency = 1.0

            test = Test( )

            test.frequency = 0.5

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-31.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import numpy


class IFrequency( IEqual ) :

    """ Frequency interface.
    """

    @property
    def frequency( self ) :

        """ Normalized frequency relative to Nyquist in [ -1.0, 1.0 ] ( float ).
        """

        return self._frequency

    @frequency.setter
    def frequency( self, frequency : float ) :

        if ( ( frequency < -1.0 ) or ( frequency > 1.0 ) ) :

            raise ValueError( 'Frequency = ' + str( frequency ) )

        self._frequency = frequency

    def __eq__( self, other : any ) -> bool :

        """ Equality.

            Arguments :

                other - Other ( any ).

            Returns :

                equality - Equality ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.isclose( self.frequency, other.frequency ) ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._frequency = 0.0
