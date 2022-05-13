""" **Description**
        A Goertzel filter realizes a discrete difference equation which
        approximates a discrete Fourier transform evaluated at a specified
        normalized frequency and order, consuming an incident signal and
        producing a reference signal.

        .. math::
            y_{n} = \sum_{i = 1}^{N} a_{i} y_{n-i} + \sum_{i = 0}^{N} b_{i} x_{n-i} = \sum_{i = 1}^{N} (\ a_{i} b_{0} + b_{i}\ ) s_{i,n} + b_{0} x_{n}\qquad a_{0} = 0

        .. math::
            s_{1,n+1} = \sum_{i = 1}^{N} a_{i} s_{i,n} + x_{n}\qquad\quad s_{i,n+1} = s_{i-1,n}

        .. math::
            \matrix{ a = \scriptsize{ [\ \matrix{ 0 & 2\ \cos(\ \pi\ f\ ) & -1 }\ ] } & b = \scriptsize{ [\ \matrix{ 1 & -e^{\ j\ \pi\ f\ } & 0 } }\ ] }

        At the terminus of each window length a reference signal is evaluated
        to estimate a discrete Fourier transform at a specified normalized
        frequency.

        .. math::
            H_{z} = \\frac{\sum_{i = 0}^{N} b_{i} z^{-i}}{{1 - \sum_{i = 1}^{N} a_{i} z^{-i}}}

        A Goertzel filter is normalized by incident signal length.  An incident
        signal length is is inversely proportional to a normalized frequency
        resolution.

        .. math::
            N = \\frac{2}{R}

    **Example**
       
        ::
        
            from diamondback import ComplexExponentialFilter, GoertzelFilter
            import numpy

            b = WindowFilter( 'Hann', 128 ).b
            frequency = 0.1

            # Create an instance.

            obj = GoertzelFilter( b = b, frequency = frequency )

            # Filter an incident signal.

            x = ComplexExponentialFilter( 0.0 ).filter( numpy.ones( 1024 ) * frequency ) * numpy.random.rand( 1 )[ 0 ]
            y = obj.filter( x )

    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2022 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, AI Hub, 2018-04-16.
"""

from diamondback.filters.IirFilter import IirFilter
from typing import List, Union
import math
import numpy

class GoertzelFilter( IirFilter ) :

    """ Goertzel filter.
    """

    @property
    def frequency( self ) :

        """ frequency : float - frequency normalized to Nyquist in [ -1.0, 1.0 ].
        """

        return self._frequency

    @frequency.setter
    def frequency( self, frequency : float ) :

        if ( ( frequency < -1.0 ) or ( frequency > 1.0 ) ) :
            raise ValueError( f'Frequency = {frequency}' )
        self._frequency = frequency

    def __init__( self, b : Union[ List, numpy.ndarray ], frequency : float ) -> None :

        """ Initialize.

            Arguments :
                b : Union[ List, numpy.ndarray ] - forward coefficient.
                frequency : float - frequency normalized to Nyquist in [ -1.0, 1.0 ].
        """

        if ( ( not numpy.isscalar( b ) ) and ( not isinstance( b, numpy.ndarray ) ) ) :
            b = numpy.array( list( b ) )
        if ( ( not len( b ) ) or ( not b.any( ) ) ) :
            raise ValueError( f'B = {b}' )
        if ( ( frequency < -1.0 ) or ( frequency > 1.0 ) ) :
            raise ValueError( f'Frequency = {frequency}' )
        u = numpy.array( [ 0.0, 2.0 * math.cos( math.pi * frequency ), -1.0 ] )
        v = numpy.array( [ 1.0, -numpy.exp( -1j * math.pi * frequency ), 0.0 ] )
        super( ).__init__( a = u, b = v )
        self._index, self._w = 0, numpy.array( b )
        self._frequency = frequency

    def filter( self, x : Union[ List, numpy.ndarray ] ) -> numpy.ndarray :

        """ Filters an incident signal and produces a reference signal.

            Arguments :
                x : Union[ List, numpy.ndarray ] - incident signal.

            Returns :
                y : numpy.ndarray - reference signal.
        """

        if ( ( not numpy.isscalar( x ) ) and ( not isinstance( x, numpy.ndarray ) ) ) :
            x = numpy.array( list( x ) )
        if ( not len( x ) ) :
            raise ValueError( f'X = {x}' )
        y = numpy.zeros( int( numpy.ceil( len( x ) / len( self._w ) ) ) + 1, complex )
        u = ( 1.0 + int( not isinstance( x[ 0 ], complex ) ) ) / len( self._w )
        jj = 0
        for ii in range( 0, len( x ) ) :
            v = super( ).filter( u * self._w[ self._index ] * x[ ii : ii + 1 ] )
            self._index += 1
            if ( self._index >= len( self._w ) ) :
                y[ jj ] = v[ 0 ]
                self.s[ : ] = 0.0
                self._index = 0
                jj += 1
        if ( jj != len( y ) ) :
            y = y[ : jj ]
        return y
