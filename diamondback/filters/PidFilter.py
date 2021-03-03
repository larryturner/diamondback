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

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-31.

    **Definition**

"""

from diamondback.filters.FirFilter import FirFilter
import numpy


class PidFilter( FirFilter ) :

    """ Proportional Integral Derivative ( PID ) filter.
    """

    @property
    def limit( self ) :

        """ Integral limit ( float ).
        """

        return self._limit

    @limit.setter
    def limit( self, limit : float ) :

        if ( limit < 0.0 ) :

            raise ValueError( f'Limit = { limit }' )

        self._limit = limit

    def __eq__( self, other : any ) -> bool :

        """ Equality.

            Arguments :

                other - Other ( any ).

            Returns :

                equality - Equality ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.isclose( self.limit, other.limit ) ) )

    def __init__( self, b : any ) -> None :

        """ Initialize.

            Arguments :

                b - Forward coefficient ( array( complex | float ), list( complex | float ) ).
        """

        if ( ( not numpy.isscalar( b ) ) and ( not isinstance( b, numpy.ndarray ) ) ) :

            b = numpy.array( list( b ) )

        if ( ( len( b.shape ) != 1 ) or ( len( b ) != 3 ) ) :

            raise ValueError( f'B = { b }' )

        super( ).__init__( b, numpy.zeros( len( b ) ), 0.0 )

        self._limit = float( 'inf' )

    def filter( self, x : any, d : any = None ) -> any :

        """ Filters an incident signal and produces a reference signal.

            Arguments :

                x - Incident signal ( array( complex | float ), list( complex | float ) ).

            Returns :

                y - Reference signal ( array( complex | float ) ).
        """

        if ( ( not numpy.isscalar( x ) ) and ( not isinstance( x, numpy.ndarray ) ) ) :

            x = numpy.array( list( x ) )

        if ( ( len( x.shape ) != 1 ) or ( len( x ) == 0 ) ) :

            raise ValueError( f'X = { x }' )

        y = numpy.zeros( len( x ), type( self.b[ 0 ] ) )

        for ii in range( 0, len( x ) ) :

            self.s[ 2 ] = x[ ii ] - self.s[ 0 ]

            if ( abs( self.s[ 1 ] + x[ ii ] ) < self.limit ) :

                self.s[ 1 ] += x[ ii ]

            self.s[ 0 ] = x[ ii ]

            y[ ii ] = self.b.dot( self.s )

        return y
