""" **Description**

        A polynomial rate filter produces a reference signal which approximates
        an incident signal evaluated at an effective frequency equal to the
        product of an incident sample frequency and a specified rate.

        A polynomial rate filter synthesizes a sequence of polynomials which
        form local approximations to an incident signal, and are evaluated at
        indices corresponding to a specified rate to produce a reference
        signal, effectively modifying the sampling rate by a specified rate
        ratio.

        A specified rate must be greater than zero, supporting decimation and
        interpolation.

        Latency compensation is not necessary, as no group delay is introduced.

        Edge effects are internally mitigated by linear extension of an
        incident signal.

        A polynomial rate filter may be the most appropriate option in
        applications which require fractional decimation and interpolation and
        benefit from minimization of edge effects due to discontinuous
        operation or dynamic rate.

    **Example**

        ::

            from diamondback import ComplexExponentialFilter, PolynomialRateFilter
            import math
            import numpy


            # Create an instance with rate and order.

            obj = PolynomialRateFilter( rate = math.pi, order = 3 )

            # Filter an incident signal.

            x = ComplexExponentialFilter( 0.0 ).filter( numpy.ones( 128 ) * 0.1 ).real

            y = obj.filter( x )

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-03-19.

    **Definition**

"""

from diamondback.interfaces.IRate import IRate
import numpy
import typing


class PolynomialRateFilter( IRate ) :

    """ Polynomial rate filter.
    """

    @property
    def order( self ) :

        """ order : int - in [ 2, inf ).
        """

        return self._order

    @order.setter
    def order( self, order : int ) :

        if ( order < 2 ) :

            raise ValueError( f'Order = {order}' )

        self._order = order

    @IRate.rate.setter
    def rate( self, rate : float ) :

        """ rate : float - ratio of effective frequency in ( 0.0, inf ).
        """

        if ( rate <= 0.0 ) :

            raise ValueError( f'Rate = {rate}' )

        if ( not numpy.isclose( self.rate, rate ) ) :

            self._index = 0.0

        IRate.rate.fset( self, rate )

    def __eq__( self, other : typing.Any ) -> bool :

        """ Equal.

            Arguments :

                other : typing.Any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.isclose( self._index, other._index ) ) and ( self.order == other.order ) )

    def __init__( self, rate : float, order : int = 3 ) -> None :

        """ Initialize.

            Arguments :

                rate : float - ratio of effective frequency in [ 1.0, inf ).

                order : int - in [ 2 , inf ).
        """

        if ( order < 2 ) :

            raise ValueError( f'Order = {order}' )

        super( ).__init__( )

        self._index, self._order = 0.0, order

        self.rate = rate

    def filter( self, x : typing.Union[ typing.List, numpy.ndarray ] ) -> numpy.ndarray :

        """ Filters an incident signal and produces a reference signal.

            Arguments :

                x : typing.Union[ typing.List, numpy.ndarray ] - incident signal.

            Returns :

                y : numpy.ndarray - reference signal.
        """

        if ( ( not numpy.isscalar( x ) ) and ( not isinstance( x, numpy.ndarray ) ) ) :

            x = numpy.array( list( x ) )

        if ( ( len( x.shape ) != 1 ) or ( len( x ) < 2 ) ) :

            raise ValueError( f'X = {x}' )

        cc = len( x )

        x = numpy.concatenate( ( [ 2.0 * x[ 0 ] - x[ 1 ] ], x, [ 2.0 * x[ -1 ] - x[ -2 ], 3.0 * x[ -1 ] - 2.0 * x[ -2 ] ] ) )

        y = numpy.zeros( int( numpy.ceil( cc * self.rate ) ) )

        eps, u, v = numpy.finfo( float ).eps, numpy.linspace( -1.0, 2.0, 4 ), 1.0 / self.rate

        ii, jj = 0, 0

        while ( ii < cc ) :

            if ( self._index < ( 1.0 - eps ) ) :

                b = numpy.polyfit( u, x[ ii : ii + 4 ], self.order )

                while ( ( self._index < ( 1.0 - eps ) ) and ( jj < len( y ) ) ) :

                    y[ jj ] = numpy.polyval( b, self._index )

                    self._index += v

                    jj += 1

            self._index -= 1.0

            ii += 1

        return y[ 0 : min( jj, len( y ) ) ]
