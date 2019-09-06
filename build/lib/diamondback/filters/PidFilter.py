""" **Description**

        A Proportional Integral Derivative ( PID ) filter realizes a discrete
        difference equation as a function of a forward coefficient array and a
        state array of a static order.  A forward coefficient array applies a
        gain to proportional, integral, and derivative representations of an
        incident signal, producing a reference signal.  An integral limit is
        specified, preventing integral saturation which may adversely affect
        control stability and latency. ::

            y,n = b,0 * x,n + b,1 * min( integral( x,n ), limit ) + b,2 * derivative( x,n )

    **Example**

        ::

            from diamondback.filters.ComplexExponentialFilter import ComplexExponentialFilter
            from diamondback.filters.PidFilter import PidFilter
            import numpy


            # Create an instance with coefficients.

            obj = PidFilter( b = numpy.array( [ 0.1, 5.0e-2, 0.0 ] ) )

            # Filter an incident signal.

            x = ComplexExponentialFilter( 0.0 ).filter( numpy.linspace( -1.0e-4, 1.0e-4, 128 ) * 0.1 ).real

            y = obj.filter( x )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

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
    def limit( self, limit ) :

        if ( limit < 0.0 ) :

            raise ValueError( 'limit = ' + str( limit ) )

        self._limit = limit

    def __eq__( self, other ) :

        """ Evaluates equality condition.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.isclose( self.limit, other.limit ) ) )

    def __init__( self, b ) :

        """ Initializes an instance.

            Arguments :

                b - Forward coefficient ( array( complex | float ), list( complex | float ) ).
        """

        if ( ( not numpy.isscalar( b ) ) and ( not isinstance( b, numpy.ndarray ) ) ) :

            b = numpy.array( list( b ) )

        if ( ( len( b.shape ) != 1 ) or ( len( b ) != 3 ) ) :

            raise ValueError( 'b = ' + str( b ) )

        super( ).__init__( b, numpy.zeros( len( b ) ), 0.0 )

        self._limit = float( 'inf' )

    def filter( self, x, d = None ) :

        """ Filters an incident signal and produces a reference signal.

            Arguments :

                x - Incident signal ( array( complex | float ), list( complex | float ) ).

            Returns :

                y - Reference signal ( array( complex | float ) ).
        """

        if ( ( not numpy.isscalar( x ) ) and ( not isinstance( x, numpy.ndarray ) ) ) :

            x = numpy.array( list( x ) )

        if ( ( len( x.shape ) != 1 ) or ( len( x ) == 0 ) ) :

            raise ValueError( 'x = ' + str( x ) )

        y = numpy.zeros( len( x ), type( self.b[ 0 ] ) )

        for ii in range( 0, len( x ) ) :

            self.s[ 2 ] = x[ ii ] - self.s[ 0 ]

            if ( abs( self.s[ 1 ] + x[ ii ] ) < self.limit ) :

                self.s[ 1 ] += x[ ii ]

            self.s[ 0 ] = x[ ii ]

            y[ ii ] = self.b.dot( self.s )

        return y
