""" **Description**

        An integral filter realizes a discrete difference equation which
        approximates a discrete integral as a function of a recursive coefficient
        array, a forward coefficient array, and a state array of a specified order,
        consuming an incident signal and producing a reference signal.  An integral
        is approximated relative to a sample.  An integral is electively approximated
        relative to a second by dividing a reference signal by an absolute sampling
        frequency.

        .. math::

            y_{n} = \sum_{i = 1}^{N} a_{i} y_{n-i} + \sum_{i = 0}^{N} b_{i} x_{n-i} = \sum_{i = 1}^{N} (\ a_{i} b_{0} + b_{i}\ ) s_{i,n} + b_{0} x_{n}\qquad a_{0} = 0

        .. math::

            s_{1,n+1} = \sum_{i = 1}^{N} a_{i} s_{i,n} + x_{n}\qquad\quad s_{i,n+1} = s_{i-1,n}

        A frequency response is expressed as a function of a recursive coefficient
        array and a forward coefficient array.

        .. math::

            H_{z} = \\frac{\sum_{i = 0}^{N} b_{i} z^{-i}}{{1 - \sum_{i = 1}^{N} a_{i} z^{-i}}}

        A factory is defined to facilitate construction of an instance, defining
        a recursive coefficient array, a forward coefficient array, and a state
        array of a specified order, to satisfy specified constraints.  An instance
        and order are specified.

        .. math::

            y_{n} = \\frac{1}{f}\ \sum_{i=0}^{N} x_{n}\quad\quad\quad\quad\scriptsize{ f = 1.0 }

        .. math::

            \matrix{ a_{1,0} = \scriptsize{ [ \matrix{ 0 & 1 } ] } & b_{1,0} = \scriptsize{ [ \matrix{ 1 } ] } }\quad\quad\scriptsize{ Rectangular }

        .. math::

            \matrix{ a_{1,1} = \scriptsize{ [ \matrix{ 0 & 1 } ] } & b_{1,1} = \scriptsize{ [ \matrix{ 1 & 1 } ]\ \\frac{1}{2} } }\quad\quad\scriptsize{ Trapezoidal }

        .. math::

            \matrix{ a_{1,2} = \scriptsize{ [ \matrix{ 0 & 1 } ] } & b_{1,2} = \scriptsize{ [ \matrix{ 1 & 4 & 1 } ]\ \\frac{1}{6} } }\quad\quad\scriptsize{ Simpson 2 }

        .. math::

            \matrix{ a_{1,3} = \scriptsize{ [ \matrix{ 0 & 1 } ] } & b_{1,3} = \scriptsize{ [ \matrix{ 1 & 3 & 3 & 1 } ]\ \\frac{1}{8} } }\quad\quad\scriptsize{ Simpson 3 }

        .. math::

            \matrix{ a_{1,4} = \scriptsize{ [ \matrix{ 0 & 1 } ] } & b_{1,4} = \scriptsize{ [ \matrix{ 7 & 32 & 12 & 32 & 7 } ]\ \\frac{1}{90} } }\quad\quad\scriptsize{ Newton Coats }

    **Example**

        ::

            from diamondback.filters.ComplexExponentialFilter import ComplexExponentialFilter
            from diamondback.filters.IntegralFilter import IntegralFilter
            import numpy


            # Create an instance from a Factory with constraints.

            obj = IntegralFilter.Factory.instance( typ = IntegralFilter, order = 2 )

            # Filter an incident signal.

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
