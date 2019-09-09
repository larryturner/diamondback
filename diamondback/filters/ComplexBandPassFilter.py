""" **Description**

        A complex band pass filter produces a complex exponential incident
        signal at a specified normalized frequency and adapts a forward complex
        coefficient to produce a reference signal, which estimates a component
        of interest in a primary signal.  A normalized frequency and rate of
        adaptation are specified.

        .. math::

            x_{n} = e^{\ j\ \pi\ \phi_{n}}

        .. math::

            \phi_{n+1} = \phi_{n} + f_{n}

        .. math::

            y_{n} = b_{n} x_{n}

        .. math::

            e_{n} = d_{n} - y_{n}

        .. math::

            b_{n+1} = b_{n} + \mu e_{n} x_{n}^{*}

    **Example**

        ::

            from diamondback.filters.ComplexBandPassFilter import ComplexBandPassFilter
            from diamondback.filters.ComplexExponentialFilter import ComplexExponentialFilter
            import numpy


            frequency = 0.1

            x = numpy.linspace( -1.0e-4, 1.0e-4, 128 ) + frequency

            # Create a primary signal.

            d = ComplexExponentialFilter( phase = numpy.random.rand( 1 )[ 0 ] * 2.0 - 1.0 ).filter( x )

            obj = ComplexBandPassFilter( frequency = frequency, rate = 5.0e-2 )

            # Filter a primary signal.

            obj.reset( d[ 0 ] )

            y, e, b = obj.filter( d )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-31.

    **Definition**

"""

from diamondback.filters.ComplexExponentialFilter import ComplexExponentialFilter
from diamondback.filters.FirFilter import FirFilter
from diamondback.interfaces.IFrequency import IFrequency
import numpy


class ComplexBandPassFilter( FirFilter, IFrequency ) :

    """ Complex band pass filter.
    """

    def __eq__( self, other ) :

        """ Evaluates equality condition.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self._complexexponentialfilter == other._complexexponentialfilter ) )

    def __init__( self, frequency, rate ) :

        """ Initializes an instance.

            Arguments :

                frequency - Normalized frequency relative to Nyquist in [ -1.0, 1.0 ) ( float ).

                rate - Rate of adaptation in [ 0.0, 1.0 ] ( float ).
        """

        super( ).__init__( numpy.array( [ numpy.finfo( float ).eps + 0j ] ), numpy.zeros( 1, complex ), rate )

        self._complexexponentialfilter = ComplexExponentialFilter( )

        self.frequency = frequency

    def filter( self, d, x = None ) :

        """ Filters an incident signal and produces a reference signal.

            Arguments :

                d - Primary signal ( array( complex | float ), list( complex | float ) ).

            Returns :

                y - Reference signal ( array( complex | float ) ).

                e - Error signal ( array( complex | float ) ).

                b - Forward coefficient ( array( complex ) ).
        """

        if ( ( not numpy.isscalar( d ) ) and ( not isinstance( d, numpy.ndarray ) ) ) :

            d = numpy.array( list( d ) )

        if ( ( len( d.shape ) != 1 ) or ( len( d ) == 0 ) ) :

            raise ValueError( 'd = ' + str( d ) )

        x = self._complexexponentialfilter.filter( numpy.ones( len( d ) ) * self.frequency )

        y, e, b = numpy.zeros( len( x ), complex ), numpy.zeros( len( x ), complex ), numpy.zeros( len( x ), complex )

        for ii in range( 0, len( x ) ) :

            y[ ii ] = x[ ii ] * self.b[ 0 ]

            e[ ii ] = d[ ii ] - y[ ii ]

            b[ ii ] = self.b[ 0 ]

            self.b[ 0 ] += self.rate * e[ ii ] * numpy.conjugate( x[ ii ] )

        if ( not isinstance( d[ 0 ], complex ) ) :

            y, e = y.real, e.real

        return y, e, b
