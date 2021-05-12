""" **Description**

        A Proportional Integral Derivative ( PID ) filter realizes a discrete
        difference equation as a function of a forward coefficient array and a
        state array of a static order.  A forward coefficient array applies a
        gain to proportional, integral, and derivative representations of an
        incident signal, producing a reference signal.  An integral limit is
        specified, preventing integral saturation which may adversely affect
        control stability and latency.

        .. math::

            y_{n} = b_{0}\ x_{n} + b_{1}\max(\ min( \sum_{0}^{n}\ x_{n},\ limit\ ),\ -limit\ ) + b_{2}\ \\frac{d}{dn}(\ x_{n}\ )

    **Example**

        ::

            from diamondback import ComplexExponentialFilter, PidFilter
            import numpy

            # Create an instance with coefficients.

            obj = PidFilter( b = numpy.array( [ 0.1, 5.0e-2, 0.0 ] ) )

            # Filter an incident signal.

            x = ComplexExponentialFilter( 0.0 ).filter( numpy.linspace( -1.0e-4, 1.0e-4, 128 ) * 0.1 ).real

            y = obj.filter( x )

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-31.

    **Definition**

"""

from diamondback.filters.FirFilter import FirFilter
import numpy
import typing

class PidFilter( FirFilter ) :

    """ Proportional Integral Derivative ( PID ) filter.
    """

    @property
    def limit( self ) :

        """ limit : float.
        """

        return self._limit

    @limit.setter
    def limit( self, limit : float ) :

        if ( limit < 0.0 ) :

            raise ValueError( f'Limit = {limit}' )

        self._limit = limit

    def __eq__( self, other : typing.Any ) -> bool :

        """ Equal.

            Arguments :

                other : typing.Any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.isclose( self.limit, other.limit ) ) )

    def __init__( self, b : typing.Union[ typing.List, numpy.ndarray ] ) -> None :

        """ Initialize.

            Arguments :

                b : typing.Union[ typing.List, numpy.ndarray ] - forward coefficient.
        """

        if ( ( not numpy.isscalar( b ) ) and ( not isinstance( b, numpy.ndarray ) ) ) :

            b = numpy.array( list( b ) )

        if ( ( len( b.shape ) != 1 ) or ( len( b ) != 3 ) ) :

            raise ValueError( f'B = {b}' )

        super( ).__init__( b, numpy.zeros( len( b ) ) )

        self._limit = float( 'inf' )

    def filter( self, x : typing.Union[ typing.List, numpy.ndarray ] ) -> numpy.ndarray :

        """ Filters an incident signal and produces a reference signal.

            Arguments :

                x : typing.Union[ typing.List, numpy.ndarray ] - incident signal.

            Returns :

                y : numpy.ndarray - reference signal.
        """

        if ( ( not numpy.isscalar( x ) ) and ( not isinstance( x, numpy.ndarray ) ) ) :

            x = numpy.array( list( x ) )

        if ( ( len( x.shape ) != 1 ) or ( len( x ) == 0 ) ) :

            raise ValueError( f'X = {x}' )

        y = numpy.zeros( len( x ), type( self.b[ 0 ] ) )

        for ii in range( 0, len( x ) ) :

            self.s[ 2 ] = x[ ii ] - self.s[ 0 ]

            if ( abs( self.s[ 1 ] + x[ ii ] ) < self.limit ) :

                self.s[ 1 ] += x[ ii ]

            self.s[ 0 ] = x[ ii ]

            y[ ii ] = self.b.dot( self.s )

        return y
