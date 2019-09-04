""" **Description**

        An integral filter realizes a discrete difference equation which
        approximates a discrete integral as a function of a recursive coefficient
        array, a forward coefficient array, and a state array of a specified order,
        consuming an incident signal and producing a reference signal.  An integral
        is approximated relative to a sample.  An integral is electively approximated
        relative to a second by dividing a reference signal by an absolute sampling
        frequency. ::

            y,n = sum( a,i,n * y,n-i ) + sum( b,i,n * x,n-i )  i : [ 0, N ]

                = sum( ( a,i,n * b,0,n + b,i,n ) * s,i,n ) + b,0,n * x,n

            a,i,n = 0.0                                        i != 1

            a,1,n = 1.0

            s,1,n+1 = a,i,n * s,i,n + x,n

            s,i,n+1 = s,i-1,n

        A frequency response is expressed as a function of a recursive coefficient
        array and a forward coefficient array. ::

            H,z,n = sum( b,i,n * z**-i ) / ( 1.0 - sum( a,i,n * z**-i ) )

        A factory is defined to facilitate construction of an instance, defining
        a recursive coefficient array, a forward coefficient array, and a state
        array of a specified order, to satisfy specified constraints.  An instance
        and order are specified. ::

            y,n = ( 1 / f ) * integral( x,n )                  f = 1.0

            Rectangular, N = 0

                y,n = y,n-1 + x,n

            Trapezoidal, N = 1

                y,n = y,n-1 + ( 1 / 2 ) * ( x,n + x,n-1 )

            Simpson 2, N = 2

                y,n = y,n-1 + ( 1 / 6 ) * ( x,n + 4 * x,n-1 + x,n-2 )

            Simpson 3, N = 3

                y,n = y,n-1 + ( 1 / 8 ) * ( x,n + 3 * x,n-1 + 3 * x,n-2 + x,n-3 )

            Newton Coats, N = 4

                y,n = y,n-1 + ( 1 / 90 ) * ( 7 * x,n + 32 * x,n-1 + 12 * x,n-2 + 32 * x,n-3 + 7 * x,n-4 )

    **Example**

        ::

            from diamondback.filters.ComplexExponentialFilter import ComplexExponentialFilter
            from diamondback.filters.IntegralFilter import IntegralFilter
            import numpy

            obj = IntegralFilter.Factory.instance( typ = IntegralFilter, order = 2 )

            x = ComplexExponentialFilter( 0.0 ).filter( numpy.ones( 128 ) * 0.1 ).real

            y = obj.filter( x )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-02-06.

    **Definition**

"""

from diamondback.filters.IirFilter import IirFilter
import numpy


class IntegralFilter( IirFilter ) :

    """ Integral filter.
    """

    class Factory( object ) :

        """ Factory.
        """

        _b = ( numpy.array( [ 1.0 ] ),
               numpy.array( [ 1.0, 1.0 ] ) * ( 1.0 / 2.0 ),
               numpy.array( [ 1.0, 4.0, 1.0 ] ) * ( 1.0 / 6.0 ),
               numpy.array( [ 1.0, 3.0, 3.0, 1.0 ] ) * ( 1.0 / 8.0 ),
               numpy.array( [ 7.0, 32.0, 12.0, 32.0, 7.0 ] ) * ( 1.0 / 90.0 ) )

        @classmethod
        def instance( cls, typ, order ) :

            """ Constructs an instance.

                Arguments :

                    typ - Type derived from IntegralFilter ( type ).

                    order - Order ( int ).

                Returns :

                    instance - Instance ( typ( ) ).
            """

            if ( ( not typ ) or ( not issubclass( typ, IntegralFilter ) ) ) :

                raise ValueError( 'type = ' + str( typ ) )

            if ( ( order < 0 ) or ( order >= len( IntegralFilter.Factory._b ) ) ) :

                raise ValueError( 'order = ' + str( order ) )

            return typ( numpy.array( [ 0.0, 1.0 ] ), IntegralFilter.Factory._b[ order ] )

    def __init__( self, a = numpy.zeros( 1 ), b = numpy.ones( 1 ) ) :

        """ Initializes an instance.

            Arguments :

                a - Recursive coefficient ( array( complex | float ), list( complex | float ) ).

                b - Forward coefficient ( array( complex | float ), list( complex | float ) ).
        """

        super( ).__init__( a, b )

    def filter( self, x, d = None ) :

        """ Filters an incident signal and produces a reference signal.

            Arguments :

                x - Incident signal ( array( float ), list( float ) ).

            Returns :

                y - Reference signal ( array( float ) ).
        """

        return super( ).filter( x )[ 0 ]
