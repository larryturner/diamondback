""" **Description**

        A complex exponential filter produces a complex exponential reference
        signal from an incident signal equal to a specified normalized frequency.
        A normalized phase is specified. ::

            x,n = f,n

            y,n = exp( j * pi * p,n )

            p,n+1 += x,n                                       p,n : [ -1.0, 1.0 ]

    **Example** ::

        from diamondback.filters.ComplexExponentialFilter import ComplexExponentialFilter
        import numpy


        # Create an instance with phase.

        obj = ComplexExponentialFilter( phase = 0.0 )

        # Filter an incident signal.

        x = numpy.linspace( -1.0e-4, 1.0e-4, 128 ) + 0.1

        y = obj.filter( x )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-31.

    **Definition**

"""

from diamondback.interfaces.IPhase import IPhase
import math
import numpy


class ComplexExponentialFilter( IPhase ) :

    """ Complex exponential filter.
    """

    def __init__( self, phase = 0.0 ) :

        """ Initializes an instance.

            Arguments :

                phase - Normalized phase relative to pi in [ -1.0, 1.0 ] ( float ).
        """

        super( ).__init__( )

        self.phase = phase

    def filter( self, x ) :

        """ Filters an incident signal and produces a reference signal.

            Arguments :

                x - Incident signal, normalized frequency relative to Nyquist in [ -1.0, 1.0 ) ( array( float ), list( float ) ).

            Returns :

                y - Reference signal ( array( complex ) ).
        """

        if ( ( not numpy.isscalar( x ) ) and ( not isinstance( x, numpy.ndarray ) ) ) :

            x = numpy.array( list( x ) )

        if ( ( len( x.shape ) != 1 ) or ( len( x ) == 0 ) or ( abs( x ) > 1.0 ).any( ) ) :

            raise ValueError( 'x = ' + str( x ) )

        y = numpy.zeros( len( x ), complex )

        phase = self.phase

        for ii in range( 0, len( x ) ) :

            y[ ii ] = numpy.exp( 1j * math.pi * phase )

            phase += x[ ii ]

        phase = numpy.fmod( phase, 2.0 )

        if ( abs( phase ) > 1.0 ) :

            phase -= numpy.sign( phase ) * 2.0

        self.phase = phase

        return y
