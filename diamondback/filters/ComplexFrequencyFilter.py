""" **Description**
        A complex frequency filter adapts and discriminates the phase of a forward
        complex coefficient to produce a reference signal, which estimates a normalized
        frequency of a primary signal which is normalized to unity magnitude.  A
        normalized frequency and rate of adaptation are specified.

        .. math::
            f_{n} = \\frac{\\tan^{-1}(\ b_{n}\ ) }{\pi}

        .. math::
            x_{n} = \\frac{d_{n}}{|\ d_{n}\ |}

        .. math::
            y_{n} = b_{n} x_{n-1}

        .. math::
            e_{n} = d_{n} - y_{n}

        .. math::
            b_{0} = e^{\ j\ \pi\ f_{0}}

        .. math::
            b_{n+1} = b_{n} + \mu e_{n} x_{n}^{*}

    **Example**
       
        ::
        
            from diamondback import ComplexExponentialFilter
            import numpy

            x = numpy.linspace( 0.0, 0.1, 128 )

            # Create a primary signal.

            d = ComplexExponentialFilter( 0.0 ).filter( x )

            # Create an instance.

            obj = ComplexFrequencyFilter( frequency = 0.0, rate = 0.1 )

            # Filter a primary signal.

            obj.reset( d[ 0 ] )
            y, e, b = obj.filter( d )

    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2023 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, AI Hub, 2018-02-01.
"""

from diamondback.filters.FirFilter import FirFilter
from typing import List, Tuple, Union
import math
import numpy
import scipy

class ComplexFrequencyFilter( FirFilter ) :

    """ Complex frequency filter.
    """

    @property
    def frequency( self ) :

        """ frequency : float - frequency normalized to Nyquist in [ -1.0, 1.0 ].
        """

        return self._frequency

    @frequency.setter
    def frequency( self, frequency : float ) :
        if ( ( frequency < -1.0 ) or ( frequency > 1.0 ) ) :
            raise ValueError( f'Frequency = {frequency} Expected Frequency in [ -1.0, 1.0 ]' )
        self.b[ 0 ] = numpy.exp( 1j * math.pi * frequency )
        self._frequency = frequency

    @property
    def rate( self ) :

        """ rate : float - in [ 0.0, 1.0 ].
        """

        return self._rate

    @rate.setter
    def rate( self, rate : float ) :
        if ( ( rate < 0.0 ) or ( rate > 1.0 ) ) :
            raise ValueError( f'Rate = {rate} Expected Rate in [ 0.0, 1.0 ]' )
        self._rate = rate

    def __init__( self, frequency : float, rate : float ) -> None :

        """ Initialize.

            Arguments :
                frequency : float - frequency normalized to Nyquist in [ -1.0, 1.0 ).
                rate : float - in [ 0.0, 1.0 ].
        """

        if ( ( frequency < -1.0 ) or ( frequency > 1.0 ) ) :
            raise ValueError( f'Frequency = {frequency} Expected Frequency in [ -1.0, 1.0 ]' )
        if ( ( rate < 0.0 ) or ( rate > 1.0 ) ) :
            raise ValueError( f'Rate = {rate} Expected Rate in [ 0.0, 1.0 ]' )
        super( ).__init__( b = numpy.ones( 1, complex ), s = numpy.ones( 1, complex ) )
        self._frequency = frequency
        self._rate = rate

    def filter( self, d : Union[ List, numpy.ndarray ] ) -> Tuple[ numpy.ndarray, numpy.ndarray, numpy.ndarray ] :  # type: ignore

        """ Filters a primary signal and produces a reference signal.

            Signals are Hilbert transformed to complex as necessary.

            Arguments :
                d : Union[ List, numpy.ndarray ] - primary signal.

            Returns :
                y : numpy.ndarray - reference signal.
                e : numpy.ndarray - error signal.
                b : numpy.ndarray - forward coefficient.
        """

        d = numpy.array( list( d ) )
        if ( not len( d ) ) :
            raise ValueError( f'D = {d}' )
        if ( not numpy.iscomplex( d ).any( ) ) :
            d = scipy.signal.hilbert( d )
        x = abs( d )  # type: ignore
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

    def reset( self, x : complex ) -> None :

        """ Modifies a state to minimize edge effects by assuming persistent
            operation at a specified primary incident condition.

            Arguments :
                x : complex - incident signal.
        """

        if ( not numpy.isscalar( x ) ) :
            raise ValueError( f'X = {x}' )
        if ( numpy.isclose( x, 0.0 ) ) :
            self.s[ 0 ] = 1.0
        else :
            self.s[ 0 ] = x / abs( x )  # type: ignore
