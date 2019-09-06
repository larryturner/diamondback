""" **Description**

        A complex frequency filter adapts and discriminates the phase of a forward
        complex coefficient to produce a reference signal, which estimates a normalized
        frequency of a primary signal which is normalized to unity magnitude.  A
        normalized frequency and rate of adaptation are specified. ::

            f,n = angle( b,n ) / pi

            x,n = d,n / abs( d,n )

            y,n = b,n * x,n-1

            e,n = d,n - y,n

            b,0 = exp( j * pi * f,0 )

            b,n+1 = b,n + rate * e,n * conjugate( x,n-1 )

    **Example** ::

        from diamondback.filters.ComplexExponentialFilter import ComplexExponentialFilter
        import numpy


        x = numpy.linspace( 0.0, 0.1, 128 )

        # Create a primary signal.

        d = ComplexExponentialFilter( 0.0 ).filter( x )

        # Create an instance with frequency and rate.

        obj = ComplexFrequencyFilter( frequency = 0.0, rate = 0.1 )

        # Filter a primary signal.

        obj.reset( d[ 0 ] )

        y, e, b = obj.filter( d )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-02-01.

    **Definition**

"""

from diamondback.filters.FirFilter import FirFilter
from diamondback.interfaces.IFrequency import IFrequency
import math
import numpy


class ComplexFrequencyFilter( FirFilter, IFrequency ) :

    """ Complex frequency filter.
    """

    @IFrequency.frequency.setter
    def frequency( self, frequency ) :

        """ Normalized frequency relative to Nyquist in [ -1.0, 1.0 ] ( float ).
        """

        IFrequency.frequency.fset( self, frequency )

        self.b[ 0 ] = numpy.exp( 1j * math.pi * self.frequency )

    def __init__( self, frequency, rate ) :

        """ Initializes an instance.

            Arguments :

                frequency - Normalized frequency relative to Nyquist in [ -1.0, 1.0 ) ( float ).

                rate = Rate of adaptation in [ 0.0, 1.0 ] ( float ).
        """

        super( ).__init__( numpy.ones( 1, complex ), numpy.ones( 1, complex ), rate )

        self.frequency = frequency

    def filter( self, d, x = None ) :

        """ Filters an incident signal and produces a reference signal.

            Arguments :

                d = Primary signal ( array( complex ), list( complex ) ).

            Returns :

                y - Reference signal ( array( float ) ).

                e = Error signal ( array( complex ) ).

                b - Forward coefficient ( array( complex ) ).
        """

        if ( ( not numpy.isscalar( d ) ) and ( not isinstance( d, numpy.ndarray ) ) ) :

            d = numpy.array( list( d ) )

        if ( ( len( d.shape ) != 1 ) or ( len( d ) == 0 ) or ( not isinstance( d[ 0 ], complex ) ) ) :

            raise ValueError( 'd = ' + str( d ) )

        x = abs( d )

        x[ numpy.isclose( x, 0.0 ) ] = 1.0

        x = d / x

        y, e, b = numpy.zeros( len( x ) ), numpy.zeros( len( x ), complex ), numpy.zeros( len( x ), complex )

        for ii in range( 0, len( x ) ) :

            y[ ii ] = numpy.angle( self.b[ 0 ] ) / math.pi

            e[ ii ] = x[ ii ] - self.b[ 0 ] * self.s[ 0 ]

            b[ ii ] = self.b[ 0 ]

            self.b[ 0 ] += self.rate * e[ ii ] * numpy.conjugate( self.s[ 0 ] )

            self.s[ 0 ] = x[ ii ]

        return y, e, b

    def reset( self, x ) :

        """ Modifies a state to minimize edge effects by assuming persistent
            operation at a specified primary incident condition.

            Arguments :

                x - Incident signal ( complex ).
        """

        if ( not numpy.isscalar( x ) ) :

            raise ValueError( 'x = ' + str( x ) )

        if ( numpy.isclose( x, 0.0 ) ) :

            self.s[ 0 ] = 1.0

        else :

            self.s[ 0 ] = x / abs( x )
