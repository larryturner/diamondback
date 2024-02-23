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

            b_{k,i} = b^{M}[\\ k (\\ N\\ +\\ 1\\ )\\ +\\ i\\ ] \\qquad\\qquad k\\ :\\ [\\ 0,\\ K\\sim 256\\ )\\qquad\\ i\\ :\\ [\\ 0,\\ N\\sim 15 \\ ]

        .. math::

            y_{n} = \\sum_{i = 0}^{N} b_{k_{n},i}\\ x_{n-i} = \\sum_{i = 1}^{N} b_{k_{n},i}\\ s_{i,n} + b_{k_{n},0}\\ x_{n}

        .. math::

            s_{1,n+1} = x_{n}\\quad\\quad s_{i,n+1} = s_{i-1,n}

        A specified rate must be greater than zero, and less than or equal to
        the quantity of filters comprising a polyphase filter bank, supporting
        decimation and interpolation.

        Phase dither is present for a real rate, though error is accumulated to
        ensure that the specified rate is realized without bias.  Group delay
        may be addressed by latency compensation.

        .. math::

            \\phi_{n+1,Rate} = \\phi_{n,Rate}\\ +\\ \\frac{K}{\\scriptsize{Rate}}

        .. math::

            \\phi_{n+1,Rate}\\ \\geq\\ K\\qquad\\longrightarrow\\qquad \\phi_{n+1,Rate} = \\phi_{n+1,Rate}\\ -\\ K

        .. math::

            k_{n+1} = \\mod(\\ \\lfloor{\\ k_{n}\\ +\\ \\phi_{n+1,Rate}}\\rfloor,\\ M\\ )

        A reset may minimize edge effects at a discontinuity by assuming
        persistent operation at a specified incident signal condition.  Edge
        extension may also be applied to an incident signal.

        A polyphase rate filter may be the most appropriate option in
        applications which require fractional decimation and interpolation and
        are not highly sensitive to minimization of edge effects or latency due
        to continuous operation.

    **Example**

        .. code-block:: python

            from diamondback import ComplexExponentialFilter, PolyphaseRateFilter
            import math
            import numpy

            # Create an instance.

            obj = PolyphaseRateFilter( rate = 1.0 / math.pi )

            # Filter an incident signal.

            x = ComplexExponentialFilter( 0.0 ).filter( numpy.ones( 128 ) * 0.1 ).real
            obj.reset( x[ 0 ] )
            y = obj.filter( x )

    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2024 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, AI Hub, 2018-03-19.
"""

from diamondback.filters.FirFilter import FirFilter
from typing import List, Union
import numpy

class PolyphaseRateFilter( object ) :

    """ Polyphase rate filter.
    """

    B = numpy.zeros( ( 256, 15 ) )

    @property
    def b( self ) :
        return PolyphaseRateFilter.B

    @property
    def rate( self ) :
        return self._rate

    @rate.setter
    def rate( self, rate : float ) :
        if ( ( rate < 0.0 ) or ( rate > PolyphaseRateFilter.B.shape[ 0 ] ) ) :
            raise ValueError( f'Rate = {rate} Expected Rate in [ 0.0, {PolyphaseRateFilter.B.shape[ 0 ]} ]' )
        if ( not numpy.isclose( self.rate, rate ) ) :
            self._index = 0.0
        self._rate = rate

    @property
    def s( self ) :
        return self._s

    @s.setter
    def s( self, s : Union[ List, numpy.ndarray ] ) :
        self._s = s

    def __init__( self, rate : float ) -> None :

        """ Initialize.

            Arguments :
                rate : float - ratio of effective frequency in ( 0.0, b.shape[ 0 ] ].
        """

        if ( ( rate < 0.0 ) or ( rate > PolyphaseRateFilter.B.shape[ 0 ] ) ) :
            raise ValueError( f'Rate = {rate} Expected Rate in [ 0.0, {PolyphaseRateFilter.B.shape[ 0 ]} ]' )
        super( ).__init__( )
        b = PolyphaseRateFilter.B
        rr, cc = b.shape
        if ( not b.any( ) ) :
            firfilter = FirFilter( style = 'Hann', frequency = 0.85 / rr, order = cc * rr - 1 )
            b = numpy.reshape( firfilter.b, ( rr, cc ), 'F' )
            for ii in range( 0, rr ) :
                b[ ii, : ] /= sum( b[ ii, : ] )
            PolyphaseRateFilter.B = b
        self._index = 0
        self._rate = rate
        self._s = numpy.zeros( cc )

    def filter( self, x : Union[ List, numpy.ndarray ] ) -> numpy.ndarray :

        """ Filters an incident signal and produces a reference signal.

            Arguments :
                x : Union[ List, numpy.ndarray ] - incident signal.

            Returns :
                y : numpy.ndarray - reference signal.
        """

        if ( not isinstance( x, numpy.ndarray ) ) :
            x = numpy.array( list( x ) )
        if ( not len( x ) ) :
            raise ValueError( f'X = {x}' )
        y = numpy.zeros( int( numpy.round( len( x ) * self.rate ) ) )
        b = PolyphaseRateFilter.B
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
        return y[ : min( jj, len( y ) ) ]

    def reset( self, x : float ) -> None :

        """ Modifies a state to minimize edge effects by assuming persistent
            operation at a specified incident signal condition.

            Arguments :
                x : float - incident signal.
        """

        if ( not numpy.isscalar( x ) ) :
            raise ValueError( f'X = {x}' )
        if ( len( self.s ) > 1 ) :
            self.s.fill( x )
