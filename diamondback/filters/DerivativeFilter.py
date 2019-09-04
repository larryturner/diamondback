""" **Description**

        A derivative filter realizes a discrete difference equation which
        approximates a discrete derivative as a function of a forward coefficient
        array and a state array of a specified order, consuming an incident signal
        and producing a reference signal.  A derivative is approximated relative
        to a sample.  A derivative is electively approximated relative to a second
        by multiplying a reference signal by an absolute sampling frequency raised
        to a derivative power. ::

            y,n = sum( b,i,n * x,n-i )                         i : [ 0, N ]

            s,1,n+1 = x,n

            s,i,n+1 = s,i-1,n

        A frequency response is expressed as a function of a forward coefficient
        array. ::

            H,z = sum( b,k * z**-k )

        A factory is defined to facilitate construction of an instance, defining
        a forward coefficient array and a state array of a specified order, to
        satisfy specified constraints.  An instance, derivative, and order are
        specified.

        Derivative is in [ 1, 3 ]. ::

            y,n = ( f**D ) * derivative( x,n, D )              f = 1.0

            D, N = 1, 1

                y,n = ( x,n - x,n-1 )

            D, N = 1, 2

                y,n = ( 1 / 2 ) * ( x,n - x,n-2 )

            D, N = 1, 4

                y,n = ( 1 / 12 ) * ( -x,n + 8 * x,n-1 - 8 * x,n-3 + x,n-4 )

            D, N = 2, 2

                y,n = ( x,n - 2 * x,n-1 + x,n-2 )

            D, N = 2, 4

                y,n = ( 1 / 4 ) * ( x,n - 2 * x,n-2 + x,n-4 )

            D, N = 2, 6

                y,n = ( 1 / 24 ) * ( -x,n + 8 * x,n-1 + x,n-2 - 16 * x,n-3 + x,n-4 + 8 * x,n-5 - x,n-6 )

            D, N = 2, 8

                y,n = ( 1 / 144 ) * ( x,n - 16 * x,n-1 + 64 * x,n-2 + 16 * x,n-3 - 130 * x,n-4 + 16 * x,n-5 + 64 * x,n-6 - 16 * x,n-7 + x,n-8 )

            D, N = 3, 4

                y,n = ( 1 / 2 ) * ( x,n - 2 * x,n-1 + 2 * x,n-3 - x,n-4 )

            D, N = 3, 6

                y,n = ( 1 / 8 ) * ( x,n - 3 * x,n-2 + 3 * x,n-4 - x,n-6 )

            D, N = 3, 8

                y,n = ( 1 / 48 ) * ( -x,n + 8 * x,n-1 + 2 * x,n-2 - 24 * x,n-3 + 24 * x,n-5 - 2 * x,n-6 - x,n-7 + x,n-8 )

    **Example**

        ::

            from diamondback.filters.ComplexExponentialFilter import ComplexExponentialFilter
            from diamondback.filters.DerivativeFilter import DerivativeFilter
            import numpy

            obj = DerivativeFilter.Factory.instance( typ = DerivativeFilter, derivative = 1, order = 2 )

            x = ComplexExponentialFilter( 0.0 ).filter( numpy.ones( 128 ) * 0.1 ).real

            obj.reset( x[ 0 ] )

            y = obj.filter( x )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-02-06.

    **Definition**

"""

from diamondback.filters.FirFilter import FirFilter
import numpy


class DerivativeFilter( FirFilter ) :

    """ Derivative filter.
    """

    class Factory( object ) :

        """ Factory.
        """

        _b = { 1 : { 1 : numpy.array( [ 1.0, -1.0 ] ),
                     2 : numpy.array( [ 1.0, 0.0, -1.0 ] ) * ( 1.0 / 2.0 ),
                     4 : numpy.array( [ -1.0, 8.0, 0.0, -8.0, 1.0 ] ) * ( 1.0 / 12.0 ) },
               2 : { 2 : numpy.array( [ 1.0, -2.0, 1.0 ] ),
                     4 : numpy.array( [ 1.0, 0.0, -2.0, 0.0, 1.0 ] ) * ( 1.0 / 4.0 ),
                     6 : numpy.array( [ -1.0, 8.0, 1.0, -16.0, 1.0, 8.0, -1.0 ] ) * ( 1.0 / 24.0 ),
                     8 : numpy.array( [ 1.0, -16.0, 64.0, 16.0, -130.0, 16.0, 64.0, -16.0, 1.0 ] ) * ( 1.0 / 144.0 ) },
               3 : { 4 : numpy.array( [ 1.0, -2.0, 0.0, 2.0, -1.0 ] ) * ( 1.0 / 2.0 ),
                     6 : numpy.array( [ 1.0, 0.0, -3.0, 0.0, 3.0, 0.0, -1.0 ] ) * ( 1.0 / 8.0 ),
                     8 : numpy.array( [ -1.0, 8.0, 2.0, -24.0, 0.0, 24.0, -2.0, -8.0, 1.0 ] ) * ( 1.0 / 48.0 ) } }

        @classmethod
        def instance( cls, typ, derivative, order ) :

            """ Constructs an instance.

                Arguments :

                    typ - Type derived from DerivativeFilter ( type ).

                    derivative - Derivative in [ 1, 3 ]  ( int ).

                    order - Order ( int ).

                Returns :

                    instance - Instance ( typ( ) ).
            """

            if ( ( not typ ) or ( not issubclass( typ, DerivativeFilter ) ) ) :

                raise ValueError( 'type = ' + str( typ ) )

            if ( derivative not in DerivativeFilter.Factory._b ) :

                raise ValueError( 'derivative = ' + str( derivative ) )

            b = DerivativeFilter.Factory._b[ derivative ]

            if ( order not in b ) :

                raise ValueError( 'order = ' + str( order ) )

            return typ( b[ order ] )

    def __init__( self, b = numpy.ones( 1 ) ) :

        """ Initializes an instance.

            Arguments :

                b - Forward coefficient ( array( complex | float ), list( complex | float ) ).
        """

        super( ).__init__( b )

    def filter( self, x, d = None ) :

        """ Filters an incident signal and produces a reference signal.

            Arguments :

                x - Incident signal ( array( float ), list( float ) ).

            Returns :

                y - Reference signal ( array( float ) ).
        """

        return super( ).filter( x )[ 0 ]
