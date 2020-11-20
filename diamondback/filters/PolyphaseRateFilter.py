""" **Description**

        A polyphase rate filter produces a reference signal which approximates
        an incident signal evaluated at an effective frequency equal to the
        product of an incident sample frequency and a specified rate.

        A polyphase rate filter synthesizes a polyphase filter bank with
        comprised of a sequence of low pass filters.  Each low pass filter in a
        filter bank realizes a common frequency response, with a fractional
        sample difference in group delay.  A stride is defined to be dependent
        upon a specified rate ratio and count.  An incident signal is filtered
        to reduce aliasing and decimated or interpolated to produce a reference
        signal, effectively modifying the sampling rate by a specified rate
        ratio.

        .. math::

            b_{k,i} = b^{M}[\ k (\ N\ +\ 1\ )\ +\ i\ ] \qquad\qquad k\ :\ [\ 0,\ K\sim 256\ )\qquad\ i\ :\ [\ 0,\ N\sim 15 \ ]

        .. math::

            y_{n} = \sum_{i = 0}^{N} b_{k_{n},i}\ x_{n-i} = \sum_{i = 1}^{N} b_{k_{n},i}\ s_{i,n} + b_{k_{n},0}\ x_{n}

        .. math::

            s_{1,n+1} = x_{n}\quad\quad s_{i,n+1} = s_{i-1,n}

        A specified rate must be greater than zero, and less than or equal to
        the quantity of filters comprising a polyphase filter bank, supporting
        decimation and interpolation.

        Phase dither is present for a real rate, though error is accumulated to
        ensure that the specified rate is realized without bias.  Group delay
        may be addressed by latency compensation.

        .. math::

            \phi_{n+1,Rate} = \phi_{n,Rate}\ +\ \\frac{K}{\scriptsize{Rate}}

        .. math::

            \phi_{n+1,Rate}\ \geq\ K\qquad\longrightarrow\qquad \phi_{n+1,Rate} = \phi_{n+1,Rate}\ -\ K

        .. math::

            k_{n+1} = \mod(\ \\lfloor{\ k_{n}\ +\ \phi_{n+1,Rate}}\\rfloor,\ M\ )

        A reset may minimize edge effects at a discontinuity by assuming
        persistent operation at a specified incident signal condition.  Edge
        extension may also be applied to an incident signal.

        A polyphase rate filter may be the most appropriate option in
        applications which require fractional decimation and interpolation and
        are not highly sensitive to minimization of edge effects or have
        continuous operation.

    **Example**

        ::

            from diamondback import ComplexExponentialFilter, PolyphaseRateFilter
            import math
            import numpy


            # Create an instance with rate.

            obj = PolyphaseRateFilter( rate = 1.0 / math.pi )

            # Filter an incident signal.

            x = ComplexExponentialFilter( 0.0 ).filter( numpy.ones( 128 ) * 0.1 ).real

            obj.reset( x[ 0 ] )

            y = obj.filter( x )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-03-19.

    **Definition**

"""

from diamondback.filters.FirFilter import FirFilter
from diamondback.interfaces.IB import IB
from diamondback.interfaces.IRate import IRate
from diamondback.interfaces.IReset import IReset
from diamondback.interfaces.IS import IS
import numpy


class PolyphaseRateFilter( IB, IRate, IReset, IS ) :

    """ Polyphase rate filter.
    """

    _b = numpy.zeros( ( 256, 15 ) )

    @IB.b.getter
    def b( self ) :

        """ Forward coefficient ( array( float ) ).
        """

        return PolyphaseRateFilter._b

    @IRate.rate.setter
    def rate( self, rate : float ) :

        """ Rate ratio of effective frequency in ( 0.0, 256.0 ] ( float ).
        """

        count = PolyphaseRateFilter._b.shape[ 0 ]

        if ( ( rate <= 0.0 ) or ( rate > count ) ) :

            raise ValueError( 'Rate = ' + str( rate ) )

        if ( not numpy.isclose( self.rate, rate ) ) :

            self._index = 0.0

        IRate.rate.fset( self, rate )

    def __eq__( self, other : any ) -> bool :

        """ Equality.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.isclose( self._index, other._index ) ) )

    def __init__( self, rate : float ) -> None :

        """ Initialize.

            Arguments :

                rate - Rate ratio of effective frequency in ( 0.0, 256.0 ] ( float ).
        """

        super( ).__init__( )

        b = PolyphaseRateFilter._b

        rr, cc = b.shape

        if ( not b.any( ) ) :

            firfilter = FirFilter.Factory.instance( FirFilter, 'Hann', 0.85 / rr, cc * rr - 1 )

            b = numpy.reshape( firfilter.b, ( rr, cc ), 'F' )

            for ii in range( 0, rr ) :

                b[ ii, : ] /= sum( b[ ii, : ] )

            PolyphaseRateFilter._b = b

        self._index, self.s = 0.0, numpy.zeros( cc )
        
        self.rate = rate

    def filter( self, x : any ) -> any :

        """ Filters an incident signal and produces a reference signal.

            Arguments :

                x - Incident signal ( array( float ), list( float ) ).

            Returns :

                y - Reference signal ( array( float ) ).
        """

        if ( ( not numpy.isscalar( x ) ) and ( not isinstance( x, numpy.ndarray ) ) ) :

            x = numpy.array( list( x ) )

        if ( ( len( x.shape ) != 1 ) or ( len( x ) == 0 ) ) :

            raise ValueError( 'X = ' + str( x ) )

        y = numpy.zeros( int( numpy.ceil( len( x ) * self.rate ) ) )

        b = PolyphaseRateFilter._b

        rr = b.shape[ 0 ]

        ii, jj = 0, 0

        while ( ( ii < len( x ) ) and ( jj < len( y ) ) ) :

            if ( self._index < rr ) :

                kk = min( int( numpy.round( self._index ) ), rr - 1 )

                self._index += rr / self.rate

                self.s[ 0 ] = x[ ii ]

                y[ jj ] = b[ kk, : ].dot( self.s )

                jj += 1

            while ( ( ii < len( x ) ) and ( self._index >= rr ) ) :

                self.s[ 0 ] = x[ ii ]

                self.s[ 1 : ] = self.s[ : -1 ]

                self._index -= rr

                ii += 1

        return y[ 0 : min( jj, len( y ) ) ]

    def reset( self, x : float ) -> None :

        """ Modifies a state to minimize edge effects by assuming persistent
            operation at a specified incident signal condition.

            Arguments :

                x - Incident signal ( float ).
        """

        if ( not numpy.isscalar( x ) ) :

            raise ValueError( 'X = ' + str( x ) )

        if ( len( self.s ) > 1 ) :

            self.s.fill( x )