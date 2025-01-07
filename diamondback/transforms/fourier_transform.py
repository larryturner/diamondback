""" **Description**
        A Fourier transform converts a real or complex discrete-time incident
        signal to a complex discrete-frequency reference signal, or a complex
        discrete-frequency incident signal to a real or complex discrete-time
        reference signal, in equivalent and reversible representations.  A
        forward coefficient array is specified to define a window filter.

        Singleton.

        .. math::

            y_{k} = \\frac{1}{N}\\ \\sum_{n = 0}^{N-1} b_{n} x_{n} e^{\\frac{\\ -j\\ \\pi\\ k \\ n}{N}} = \\frac{1}{N}\\ fft(\\ x_{n}\\ )

        .. math::

            x_{n} = \\frac{N}{b_{n}}\\ \\sum_{k = 0}^{N-1} y_{k} e^{\\frac{\\ j\\ \\pi\\ k \\ n}{N}} = \\frac{N}{b_{n}}\\ ifft(\\ y_{k}\\ )

        A Fourier transform is normalized by incident signal length and forms
        a contiguous sequence corresponding to a linear and increasing
        normalized frequency.

        .. math::

            f_{k} = -1\\ + \\ 2\\ \\frac{k}{N}

        An incident signal length is inversely proportional to a normalized
        frequency resolution.

            N = \\frac{2}{R}

    **Example**

        .. code-block:: python

            from diamondback import ComplexExponentialFilter, FourierTransform
            import numpy

            x = ComplexExponentialFilter( 0.0 ).filter( numpy.linspace( 0.12, 0.23, 128 ) ) * numpy.random.rand( 1 )[ 0 ]
            b = WindowFilter( 'Hann', len( x ) - 1 ).b
            y, f = FourierTransform.transform( x, b = b, inverse = False )
            z = FourierTransform.transform( y, b = b, inverse = True )[ 0 ]

    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2024 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, AI Hub, 2018-04-12.
"""

import numpy

class FourierTransform( object ) :

    """ Fourier transform.
    """

    @staticmethod
    def transform( x : list | numpy.ndarray, b : list | numpy.ndarray, inverse : bool = False ) -> tuple[ numpy.ndarray, numpy.ndarray ] :

        """ Transforms a real or complex discrete-time incident signal to a
            complex discrete-frequency reference signal, or performs an
            inverse transform.  Indices definition depends upon an inverse
            condition.  Forward transform indices define normalized frequency.
            Inverse transform indices define an integral sequence.

            Arguments :
                x : list | numpy.ndarray - incident signal.
                b : list | numpy.ndarray - forward coefficient.
                inverse : bool.

            Returns :
                y : numpy.ndarray - reference signal.
                f : numpy.ndarray - frequency normalized to Nyquist in [ -1.0, 1.0 ).
        """

        if ( not isinstance( x, numpy.ndarray ) ) :
            x = numpy.array( list( x ) )
        if ( not len( x ) ) :
            raise ValueError( f'X = {x}' )
        if ( not isinstance( b, numpy.ndarray ) ) :
            b = numpy.array( list( b ) )
        if ( ( len( b ) > len( x ) ) or ( numpy.isclose( b, 0.0 ).all( ) ) ) :
            raise ValueError( f'B = {b}' )
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
