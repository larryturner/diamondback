""" **Description**

        Frequency interface.

    **Example**

        ::

            from diamondback.interfaces.IFrequency import IFrequency


            class Test( IFrequency ) :

                def __init__( self ) :

                    super( ).__init__( )

                    self.frequency = 0.1

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
    def frequency( self, frequency ) :

        if ( ( frequency < -1.0 ) or ( frequency > 1.0 ) ) :

            raise ValueError( 'Frequency = ' + str( frequency ) )

        self._frequency = frequency

    def __eq__( self, other ) :

        """ Evaluates equality condition.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.isclose( self.frequency, other.frequency ) ) )

    def __init__( self ) :

        """ Initializes an instance.
        """

        super( ).__init__( )

        self._frequency = 0.0
