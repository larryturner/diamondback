""" **Description**

        A Fourier transform converts a real or complex discrete-time incident
        signal to a complex discrete-frequency reference signal, or a complex
        discrete-frequency incident signal to a real or complex discrete-time
        reference signal, in equivalent and reversible representations.  A
        forward coefficient array is specified to define a window filter.

        Singleton. ::

            y,k = ( 1.0 / N ) * sum( ( b,n * x,n ) * exp( -j * pi * ( k / N ) * n ) )

                = ( 1.0 / N ) * fft( x,n )                     n, k : [ 0, N )

            f,k = -1.0 + 2.0 * ( k / N )

            x,n = N * sum( y,k * exp( j * pi * ( k / N ) * n ) ) / b,n

                = N * ifft( y,k ) / b,n

        A Fourier transform is normalized by incident signal length and forms
        a contiguous sequence corresponding to a linear and increasing
        normalized frequency.

        An incident signal length is inversely proportional to a normalized
        frequency resolution. ::

            N = 2.0 / R

    **Example** ::

        from diamondback.filters.ComplexExponentialFilter import ComplexExponentialFilter
        from diamondback.transforms.FourierTransform import FourierTransform
        import numpy


        x = ComplexExponentialFilter( 0.0 ).filter( numpy.linspace( 0.12, 0.23, 128 ) ) * numpy.random.rand( 1 )[ 0 ]

        b = WindowFilter.Factory.instance( WindowFilter, 'Hann', len( x ) - 1 ).b

        # Transform an incident signal, forward and inverse.

        y, f = FourierTransform.transform( x, b = b, inverse = False )

        z = FourierTransform.transform( y, b = b, inverse = True )[ 0 ]

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-04-12.

    **Definition**

"""

import numpy


class FourierTransform( object ) :

    """ Fourier transform.
    """

    @staticmethod
    def transform( x, b, inverse = False ) :

        """ Transforms a real or complex discrete-time incident signal to a
            complex discrete-frequency reference signal, or performs an
            inverse transform.  Indices definition depends upon an inverse
            condition.  Forward transform indices define normalized frequency.
            Inverse transform indices define an integral sequence.

            Arguments :

                x - Incident signal ( array( complex | float ), list( complex | float ) ).

                b - Forward coefficient ( array( float ), list( float ) ).

                inverse - Inverse condition ( bool ).

            Returns :

                y - Reference signal ( array( complex | float ) ).

                f - Normalized frequency relative to Nyquist in [ -1.0, 1.0 ) ( array( float ) ).
        """

        if ( ( not numpy.isscalar( x ) ) and ( not isinstance( x, numpy.ndarray ) ) ) :

            x = numpy.array( list( x ) )

        if ( ( len( x.shape ) != 1 ) or ( len( x ) == 0 ) ) :

            raise ValueError( 'x = ' + str( x ) )

        if ( ( not numpy.isscalar( b ) ) and ( not isinstance( b, numpy.ndarray ) ) ) :

            b = numpy.array( list( b ) )

        if ( ( len( b.shape ) != 1 ) or ( len( b ) > len( x ) ) or ( numpy.isclose( b[ 1 : -1 ], 0.0 ).any( ) ) ) :

            raise ValueError( 'b = ' + str( b ) )

        u = numpy.array( x[ : len( b ) ] )

        v = numpy.array( b )

        if ( inverse ) :

            if ( ( numpy.isclose( v[ 0 ], 0.0 ) ) or ( numpy.isclose( v[ -1 ], 0.0 ) ) ) :

                v[ 0 ], v[ -1 ] = v[ 1 ], v[ -2 ]

            y = numpy.concatenate( ( u[ len( u ) // 2 : ], u[ : len( u ) // 2 ] ) )

            y, f = numpy.fft.ifft( y ) * len( y ) / v, numpy.linspace( 0, len( y ) - 1, len( y ) )

        else :

            y, f = numpy.fft.fft( v * u ) / len( u ), numpy.linspace( -1.0, 1.0 - 2.0 / len( u ), len( u ) )

            y = numpy.concatenate( ( y[ len( y ) // 2 : ], y[ : len( y ) // 2 ] ) )

        return y, f
