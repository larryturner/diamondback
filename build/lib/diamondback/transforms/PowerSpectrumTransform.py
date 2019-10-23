""" **Description**

        A power spectrum transform converts a real or complex discrete-time
        incident signal to a real discrete-frequency reference signal, which
        estimates a mean power density in the incident signal relative to
        frequency.  A forward coefficient array is specified to define a window
        filter.

        Singleton.

        A power spectrum transform is constructed by estimating a mean power
        from a collection of Fourier transforms of an incident signal, over a
        sliding window defined by a forward coefficient array which defines a
        window filter.  An index specifies a sample interval, or a
        non-overlapping stride, between successive operations.

        .. math::

            v_{i,k} = \\frac{1}{N}\ \sum_{n = 0}^{N-1} b_{n} x_{n+i\ I} e^{ \\frac{\ -j\ \pi\ k \ n}{N} }

        .. math::

            y_{k} = \\frac{1}{C}\ \sum_{i = 0}^{C-1} v_{i,k} v^{*}_{i,k}

        A power spectrum transform is normalized by incident signal length and
        forms a contiguous sequence corresponding to a linear and increasing
        normalized frequency.

        .. math::

            f_{k} = -1\ + \ 2\ \\frac{k}{N}

        An incident signal length is inversely proportional to a normalized
        frequency resolution.

        .. math::

            N = \\frac{2}{R}

    **Example** ::

        from diamondback.filters.ComplexExponentialFilter import ComplexExponentialFilter
        from diamondback.transforms.PowerSpectrumTransform import PowerSpectrumTransform
        import numpy


        x = ComplexExponentialFilter( 0.0 ).filter( numpy.linspace( 0.12, 0.23, 1024 ) ) * numpy.random.rand( 1 )[ 0 ]

        b = WindowFilter.Factory.instance( WindowFilter, 'Hann', 128 - 1 ).b

        # Transform an incident signal.

        y, f = PowerSpectrumTransform.transform( x, b = b, index = len( b ) // 2 )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-04-13.

    **Definition**

"""

from diamondback.transforms.FourierTransform import FourierTransform
import numpy


class PowerSpectrumTransform( object ) :

    """ Power spectrum transform.
    """

    @staticmethod
    def transform( x, b, index ) :

        """ Transforms a real or complex discrete-time incident signal to a
            real discrete-frequency reference signal.

            Arguments :

                x - Incident signal ( array( complex | float ), list( complex | float ) ).

                b - Forward coefficient ( array( float ), list( float ) ).

                index = Index ( int ).

            Returns :

                y - Reference signal ( array( float ) ).

                f - Normalized frequency relative to Nyquist in [ -1.0, 1.0 ) ( array( float ) ).
        """

        if ( ( not numpy.isscalar( x ) ) and ( not isinstance( x, numpy.ndarray ) ) ) :

            x = numpy.array( list( x ) )

        if ( ( len( x.shape ) != 1 ) or ( len( x ) == 0 ) ) :

            raise ValueError( 'X = ' + str( x ) )

        if ( ( not numpy.isscalar( b ) ) and ( not isinstance( b, numpy.ndarray ) ) ) :

            b = numpy.array( list( b ) )

        if ( ( len( b.shape ) != 1 ) or ( len( b ) == 0 ) or ( numpy.isclose( b[ 1 : -1 ], 0.0 ).any( ) ) ) :

            raise ValueError( 'B = ' + str( b ) )

        if ( len( x ) < len( b ) ) :

            raise ValueError( 'X = ' + str( x ) )

        y, f = numpy.zeros( len( b ) ), None

        jj = 0

        for ii in range( 0, len( x ) - len( b ) + 1, index ) :

            v, f = FourierTransform.transform( x[ ii : ii + len( b ) ], b )

            y += abs( v * numpy.conjugate( v ) )

            jj += 1

        y /= jj

        return y, f
