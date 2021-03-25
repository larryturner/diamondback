""" **Description**

        A derivative filter realizes a discrete difference equation which
        approximates a discrete derivative as a function of a forward coefficient
        array and a state array of a specified order, consuming an incident signal
        and producing a reference signal.  A derivative is approximated relative
        to a sample.  A derivative is electively approximated relative to a second
        by multiplying a reference signal by an absolute sampling frequency raised
        to a derivative power.

        .. math::

            y_{n} = \sum_{i = 0}^{N} b_{i} x_{n-i} = \sum_{i = 1}^{N} b_{i} s_{i,n} + b_{0} x_{n}

            s_{1,n+1} = x_{n}\qquad\quad s_{i,n+1} = s_{i-1,n}

        A frequency response is expressed as a function of a forward coefficient
        array.

        .. math::

            H_{z} = \sum_{i = 0}^{N} b_{i} z^{-i}

        A factory is defined to facilitate construction of an instance, defining
        a forward coefficient array and a state array of a specified order, to
        satisfy specified constraints.  An instance, derivative, and order are
        specified.

        .. math::

            y_{n} = f^{D}\ \\frac{x_{n}}{D}\quad\quad\quad\quad\scriptsize{ f = 1.0 }

        .. math::

            b_{1,1} = \scriptsize{ [ \matrix{ 1 & -1 } ] }

        .. math::

            b_{1,2} = \scriptsize{ [ \matrix{ 1 & 0 & -1 } ]\ \\frac{1}{2} }

        .. math::

            b_{1,4} = \scriptsize{ [ \matrix{ -1 & 8 & 0 & -8 & 1 } ]\ \\frac{1}{12} }

        .. math::

            b_{2,2} = \scriptsize{ [ \matrix{ 1 & -2 & 1 } ] }

        .. math::

            b_{2,4} = \scriptsize{ [ \matrix{ 1 & 0 & -2 & 0 & 1 } ]\ \\frac{1}{4} }

        .. math::

            b_{2,6} = \scriptsize{ [ \matrix{ -1 & 8 & 1 & -16 & 1 & 8 & -1 } ]\ \\frac{1}{24} }

        .. math::

            b_{2,8} = \scriptsize{ [ \matrix{ 1 & -16 & 64 & 16 & -130 & 16 & 64 & -16 & 1 } ]\ \\frac{1}{144} }

        .. math::

            b_{3,4} = \scriptsize{ [ \matrix{ 1 & -2 & 0 & 2 & -1 } ]\ \\frac{1}{2} }

        .. math::

            b_{3,6} = \scriptsize{ [ \matrix{ 1 & 0 & -3 & 0 & 3 & 0 & 1 } ]\ \\frac{1}{8} }

        .. math::

            b_{3,8} = \scriptsize{ [ \matrix{ -1 & 8 & 2 & -24 & 0 & 24 & -2 & -8 & 1 } ]\ \\frac{1}{48} }

    **Example**

        ::

            from diamondback import ComplexExponentialFilter, DerivativeFilter
            import numpy


            # Create an instance from a Factory with constraints.

            obj = DerivativeFilter.Factory.instance( typ = DerivativeFilter, derivative = 1, order = 2 )

            # Filter an incident signal.

            x = ComplexExponentialFilter( 0.0 ).filter( numpy.ones( 128 ) * 0.1 ).real

            obj.reset( x[ 0 ] )

            y = obj.filter( x )

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

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
        def instance( cls, typ : type, derivative : int, order : int ) -> any :

            """ Constructs an instance.

                Arguments :

                    typ - Type derived from DerivativeFilter ( type ).

                    derivative - Derivative in [ 1, 3 ]  ( int ).

                    order - Order ( int ).

                Returns :

                    instance - Instance ( typ( ) ).
            """

            if ( ( not typ ) or ( not issubclass( typ, DerivativeFilter ) ) ) :

                raise ValueError( f'Type = {typ}' )

            if ( derivative not in DerivativeFilter.Factory._b ) :

                raise ValueError( f'Derivative = {derivative}' )

            b = DerivativeFilter.Factory._b[ derivative ]

            if ( order not in b ) :

                raise ValueError( f'Order = {order}' )

            return typ( b[ order ] )

    def __init__( self, b : any = numpy.ones( 1 ) ) -> None :

        """ Initialize.

            Arguments :

                b - Forward coefficient ( array( complex | float ), list( complex | float ) ).
        """

        super( ).__init__( b )

    def filter( self, x : any, d : any = None ) -> any :

        """ Filters an incident signal and produces a reference signal.

            Arguments :

                x - Incident signal ( array( float ), list( float ) ).

            Returns :

                y - Reference signal ( array( float ) ).
        """

        return super( ).filter( x )
