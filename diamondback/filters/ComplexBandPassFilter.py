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

            from diamondback import ComplexBandPassFilter, ComplexExponentialFilter
            import numpy

            frequency = 0.1

            x = numpy.linspace( -1.0e-4, 1.0e-4, 128 ) + frequency

            # Create a primary signal.

            d = ComplexExponentialFilter( phase = numpy.random.rand( 1 )[ 0 ] * 2.0 - 1.0 ).filter( x )

            # Create an instance with frequency and rate.

            obj = ComplexBandPassFilter( frequency = frequency, rate = 5.0e-2 )

            # Filter a primary signal.

            obj.reset( d[ 0 ] )

            y, e, b = obj.filter( d )

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-31.

    **Definition**

"""

from diamondback.filters.ComplexExponentialFilter import ComplexExponentialFilter
from diamondback.filters.FirFilter import FirFilter
from diamondback.interfaces.IFrequency import IFrequency
from diamondback.interfaces.IRate import IRate
import numpy
import typing

class ComplexBandPassFilter( FirFilter, IFrequency, IRate ) :

    """ Complex band pass filter.
    """

    def __eq__( self, other : typing.Any ) -> bool :

        """ Equal.

            Arguments :

                other : typing.Any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( self._complexexponentialfilter == other._complexexponentialfilter ) )

    def __init__( self, frequency : float, rate : float ) -> None :

        """ Initialize.

            Arguments :

                frequency : float - relative to Nyquist in [ -1.0, 1.0 ).

                rate : float - in [ 0.0, 1.0 ].
        """

        if ( ( rate < 0.0 ) or ( rate > 1.0 ) ) :

            raise ValueError( f'Rate = {rate}' )

        super( ).__init__( numpy.array( [ numpy.finfo( float ).eps + 0j ] ), numpy.zeros( 1, complex ) )

        self._complexexponentialfilter = ComplexExponentialFilter( )

        self.frequency, self.rate = frequency, rate

    def filter( self, d : typing.Union[ typing.List, numpy.ndarray ], x : typing.Union[ typing.List, numpy.ndarray ] = None ) -> typing.Tuple[ numpy.ndarray, numpy.ndarray, numpy.ndarray ] :

        """ Filters an incident signal and produces a reference signal.

            Arguments :

                d : typing.Union[ typing.List, numpy.ndarray ] - primary signal.

                x : typing.Union[ typing.List, numpy.ndarray ] - incident signal.

            Returns :

                y : numpy.ndarray - reference signal.

                e : numpy.ndarray - error signal.

                b : numpy.ndarray - forward coefficient.
        """

        if ( ( not numpy.isscalar( d ) ) and ( not isinstance( d, numpy.ndarray ) ) ) :

            d = numpy.array( list( d ) )

        if ( ( len( d.shape ) != 1 ) or ( len( d ) == 0 ) ) :

            raise ValueError( f'D = {d}' )

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
