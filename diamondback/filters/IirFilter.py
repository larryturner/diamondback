""" **Description**

        An Infinite Impulse Response ( IIR ) filter realizes a discrete
        difference equation as a function of a recursive coefficient array,
        a forward coefficient array, and a state array of a specified order,
        consuming an incident signal and producing a reference signal.

        .. math::

            y_{n} = \sum_{i = 1}^{N} a_{i,n} y_{n-i} + \sum_{i = 0}^{N} b_{i,n} x_{n-i} = \sum_{i = 1}^{N} (\ a_{i,n} b_{0,n} + b_{i,n}\ ) s_{i,n} + b_{0,n} x_{n}\qquad a_{0,n} = 0

        .. math::

            s_{1,n+1} = \sum_{i = 1}^{N} a_{i,n} s_{i,n} + x_{n}\qquad\qquad s_{i,n+1} = s_{i-1,n}

        A reset may minimize edge effects at a discontinuity by assuming
        persistent operation at a specified incident signal condition.

        .. math::

            s_{i,n} = \\frac{1.0 - b_{0,n}}{\sum_{i=1}^{N} a_{i,n} b_{0,n} + b_{i,n}}\ x_{n}

        A frequency response is expressed as a function of a recursive
        coefficient array and a forward coefficient array.

        .. math::

            H_{z,n} = \\frac{\sum_{i = 0}^{N} b_{i,n} z^{-i}}{{1 - \sum_{i = 1}^{N} a_{i,n} z^{-i}}}

        A factory is defined to facilitate construction of an instance,
        defining a recursive coefficient array, a forward coefficient array,
        and a state array of a specified order, to realize specified
        constraints.  An instance, classification, frequency, order, count,
        complement, and gain are specified.

        Frequency corresponds to a -3 dB frequency response normalized relative
        to Nyquist.

        Classification is in ( 'Bessel', 'Butterworth', 'Chebyshev' ).

        * | 'Bessel' filters demonstrate maximally linear phase response or
          | constant group delay.

        * | 'Butterworth' filters demonstrate maximally flat magnitude response.

        * | 'Chebyshev' filters demonstrate minimally low magnitude response error
          | and improved rate of attenuation in a Type I form, with a maximum in
          | band ripple of 0.125 dB.

        Count is a quantity of filters of a specified order concatenated to
        form an aggregate frequency response in cascade form.

        Complement effectively constructs a mirror image of a specified
        frequency response.

    **Example**

        ::

            from diamondback import IirFilter
            import numpy

            # Create an instance from a Factory with constraints.

            obj = IirFilter.Factory.instance( typ = IirFilter, classification = 'Chebyshev', frequency = 0.1, order = 8, count = 1 )

            # Create an instance with coefficients.

            obj = IirFilter( a = obj.a, b = obj.b )

            # Estimate frequency response, group delay, and roots.

            y, f = obj.response( length = 8192, count = 1 )

            y, f = obj.delay( length = 8192, count = 1 )

            p, z = obj.roots( count = 1 )

            # Filter an incident signal.

            x = numpy.random.rand( 128 ) * 2.0 - 1.0

            obj.reset( x[ 0 ] )

            y = obj.filter( x )

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-23.

    **Definition**

"""

from diamondback.filters.FirFilter import FirFilter
from diamondback.interfaces.IA import IA
from diamondback.transforms.ZTransform import ZTransform
from typing import Any, List, Tuple, Union
import math
import numpy
import scipy.signal
import warnings

class IirFilter( FirFilter, IA ) :

    """ Infinite Impulse Response ( IIR ) filter.
    """

    class Factory( object ) :

        """ Factory.
        """

        _classification = ( 'Bessel', 'Butterworth', 'Chebyshev' )

        @staticmethod
        def _evaluate( classification : str, frequency : float, order : int ) -> Tuple[ numpy.ndarray, numpy.ndarray ] :

            """ Evaluates coefficients.

                Arguments :

                    classification : str - in ( 'Bessel', 'Butterworth', 'Chebyshev' ).

                    frequency : float - relative to Nyquist in ( 0.0, 1.0 ).

                    order : int.

                Returns :

                    a : numpy.ndarray - recursive coefficient.

                    b : numpy.ndarray - forward coefficient.
            """

            bilinear = True

            if ( classification == 'Bessel' ) :

                bilinear = False

                u, a = numpy.ones( 1 ), numpy.ones( 2 )

                for ii in range( 2, order + 1 ) :

                    x = numpy.concatenate( ( u, numpy.zeros( 2 ) ) ) + numpy.concatenate( ( [ 0.0 ], ( ( 2.0 * ii ) - 1.0 ) * a ) )

                    u, a = a, x

            elif ( classification == 'Butterworth' ) :

                a = numpy.ones( 1 )

                for ii in range( 1, ( order // 2 ) + 1 ) :

                    a = numpy.convolve( a, numpy.array( [ 1.0, -2.0 * math.cos( ( ( ( 2.0 * ii ) + order - 1.0 ) / ( 2.0 * order ) ) * math.pi ), 1.0 ] ) )

                if ( order & 1 ) :

                    a = numpy.convolve( a, numpy.ones( 2 ) )

            elif ( classification == 'Chebyshev' ) :

                ripple = 0.125

                u = numpy.array( [ numpy.exp( 1j * math.pi * x / ( 2.0 * order ) ) for x in range( 1, 2 * order, 2 ) ] )

                v = math.asinh( 1.0 / ( ( 10.0 ** ( 0.1 * ripple ) - 1.0 ) ** 0.5 ) ) / order

                a = ( numpy.poly( ( -math.sinh( v ) * u.imag + 1j * math.cosh( v ) * u.real ) * 2.0 * math.pi ) ).real

            a /= a[ -1 ]

            a, b = ZTransform.transform( a, [ 1.0 ], frequency, bilinear )

            b = numpy.poly( -numpy.ones( order ) )

            b *= ( 1.0 - sum( a ) ) / sum( b )

            return a, b

        @classmethod
        def instance( cls, typ : type, classification : str, frequency : float, order : int, count : int = 1, complement : bool = False, gain : float = 1.0 ) -> Any :

            """ Constructs an instance.

                Arguments :

                    typ : type - derived from IirFilter.

                    classification : str - in ( 'Bessel', 'Butterworth', 'Chebyshev' ).

                    frequency : float - relative to Nyquist in ( 0.0, 1.0 ).

                    order : int.

                    count : int.

                    complement : bool.

                    gain : float.

                Returns :

                    instance : typ( ).
            """

            if ( ( not typ ) or ( not issubclass( typ, IirFilter ) ) ) :

                raise ValueError( f'Type = {typ}' )

            if ( ( not classification ) or ( classification not in IirFilter.Factory._classification ) ) :

                raise ValueError( f'Classification = {classification}' )

            if ( ( frequency <= 0.0 ) or ( frequency >= 1.0 ) ) :

                raise ValueError( f'Frequency = {frequency}' )

            if ( order <= 0 ) :

                raise ValueError( f'Order = {order}' )

            if ( count <= 0 ) :

                raise ValueError( f'Count = {count}' )

            if ( complement ) :

                frequency = 1.0 - frequency

            beta, eps, error = 10.0, numpy.finfo( float ).eps, float( 'inf' )

            index, mu, zeta = 500 * ( 1 + ( count > 2 ) ), 2.5e-2, 1.0

            a, b = [ ], [ ]

            for ii in range( 0, index ) :

                u, v = IirFilter.Factory._evaluate( classification, zeta * frequency, order )

                x = numpy.exp( 1j * math.pi * frequency )

                e = ( 2.0 ** ( -0.5 ) ) - ( ( abs( numpy.polyval( v, x ) / numpy.polyval( numpy.concatenate( ( [ 1.0 ], -u[ 1 : ] ) ), x ) ) ) ** count )

                if ( abs( e ) < error ) :

                    a, b, error = u, v, abs( e )

                    if ( error < ( 10.0 * eps ) ) :

                        break

                zeta = max( zeta + mu * math.tanh( beta * e ), eps )

            if ( complement ) :

                a *= numpy.array( [ ( ( -1.0 ) ** x ) for x in range( 0, len( a ) ) ] )

                b *= numpy.array( [ ( ( -1.0 ) ** x ) for x in range( 0, len( b ) ) ] )

                b /= sum( b * numpy.array( [ ( ( -1.0 ) ** x ) for x in range( 0, len( b ) ) ] ) ) / sum( numpy.concatenate( ( [ 1.0 ], -a[ 1 : ] ) ) * numpy.array( [ ( ( -1.0 ) ** x ) for x in range( 0, len( a ) ) ] ) )

            return typ( a, b * gain )

    def __init__( self, a : Union[ List, numpy.ndarray ] = numpy.zeros( 1 ), b : Union[ List, numpy.ndarray ] = numpy.ones( 1 ), s : Union[ List, numpy.ndarray ] = numpy.zeros( 1 ) ) -> None :

        """ Initialize.

            Arguments :

                a : Union[ List, numpy.ndarray ] - recursive coefficient, s-domain.

                b : Union[ List, numpy.ndarray ] - forward coefficient.

                s : Union[ List, numpy.ndarray ] - state.
        """

        if ( ( not numpy.isscalar( a ) ) and ( not isinstance( a, numpy.ndarray ) ) ) :

            a = numpy.array( list( a ) )

        if ( ( len( a.shape ) != 1 ) or ( ( len( a ) > 0 ) and ( a[ 0 ] ) ) ) :

            raise ValueError( f'A = {a}' )

        if ( len( a ) < len( b ) ) :

            a = numpy.concatenate( ( a, numpy.zeros( len( b ) - len( a ) ) ) )

        if ( len( b ) < len( a ) ) :

            b = numpy.concatenate( ( b, numpy.zeros( len( a ) - len( b ) ) ) )

        if ( ( isinstance( a[ 0 ], complex ) ) or ( isinstance( b[ 0 ], complex ) ) ) :

            a, b = numpy.array( a, complex ), numpy.array( b, complex )

        if ( a[ 0 ] != 0.0 ) :

            raise ValueError( f'A = {a}' )

        super( ).__init__( b, s )

        self.a = numpy.array( a )

    def delay( self, length : int = 8192, count : int = 1 ) -> Tuple[ numpy.ndarray, numpy.ndarray ] :

        """ Estimates group delay and produces a reference signal.

            Arguments :

                length : int.

                count : int.

            Returns :

                y : numpy.ndarray - reference signal.

                f : numpy.ndarray - relative to Nyquist in [ -1.0, 1.0 ).
        """

        if ( length <= 0 ) :

            raise ValueError( f'Length = {length}' )

        if ( count <= 0 ) :

            raise ValueError( f'Count = {count}' )

        with warnings.catch_warnings( ) :

            warnings.simplefilter( 'ignore' )

            y, f = scipy.signal.group_delay( ( self.b, numpy.concatenate( ( [ 1.0 ], -self.a[ 1 : ] ) ) ), length, True )[ 1 ], numpy.linspace( -1.0, 1.0 - 2.0 / length, length )

            y = numpy.concatenate( ( y[ len( y ) // 2 : ], y[ : len( y ) // 2 ] ) )

        if ( length > 2 ) :

            y[ 0 ] = y[ 1 ] * 2.0 - y[ 2 ]

        return y, f

    def filter( self, x : Union[ List, numpy.ndarray ] ) -> numpy.ndarray :

        """ Filters an incident signal and produces a reference signal.

            Arguments :

                x : Union[ List, numpy.ndarray ] - incident signal.

            Returns :

                y : numpy.ndarray - reference signal.
        """

        if ( ( not numpy.isscalar( x ) ) and ( not isinstance( x, numpy.ndarray ) ) ) :

            x = numpy.array( list( x ) )

        if ( ( len( x.shape ) != 1 ) or ( len( x ) == 0 ) ) :

            raise ValueError( f'X = {x}' )

        y = numpy.zeros( len( x ), type( self.b[ 0 ] ) )

        for ii in range( 0, len( x ) ) :

            self.s[ 0 ] = x[ ii ]

            c = self.a * self.b[ 0 ] + self.b

            y[ ii ] = c.dot( self.s )

            if ( len( self.s ) > 1 ) :

                z = self.a.dot( self.s )

                self.s[ 1 : ] = self.s[ : -1 ]

                self.s[ 1 ] += z

        return y

    def reset( self, x : Union[ complex, float ] ) -> None :

        """ Modifies a state to minimize edge effects by assuming persistent
            operation at a specified incident signal condition.

            Arguments :

                x : Union[ complex, float ] - incident signal.
        """

        if ( not numpy.isscalar( x ) ) :

            raise ValueError( f'X = {x}' )

        if ( len( self.s ) > 1 ) :

            self.s.fill( x * ( 1.0 - self.b[ 0 ] ) / ( self.a[ 1 : ] * self.b[ 0 ] + self.b[ 1 : ] ).sum( ) )

    def response( self, length = 8192, count = 1 ) -> Tuple[ numpy.ndarray, numpy.ndarray ] :

        """ Estimates frequency response and produces a reference signal.

            Arguments :

                length : int.

                count : int.

            Returns :

                y : numpy.ndarray - reference signal.

                f : numpy.ndarray - relative to Nyquist in [ -1.0, 1.0 ).
        """

        if ( length <= 0 ) :

            raise ValueError( f'Length = {length}' )

        if ( count <= 0 ) :

            raise ValueError( f'Count = {count}' )

        with warnings.catch_warnings( ) :

            warnings.simplefilter( 'ignore' )

            y, f = scipy.signal.freqz( self.b, numpy.concatenate( ( [ 1.0 ], -self.a[ 1 : ] ) ), length, True )[ 1 ], numpy.linspace( -1.0, 1.0 - 2.0 / length, length )

            y = numpy.concatenate( ( y[ len( y ) // 2 : ], y[ : len( y ) // 2 ] ) ) ** count

        return y, f

    def roots( self, count = 1 ) -> Tuple[ numpy.ndarray, numpy.ndarray ] :

        """ Estimates roots of a frequency response in poles and zeros.

            Arguments :

                count : int.

            Returns :

                p : numpy.ndarray - poles.

                z : numpy.ndarray - zeros.
        """

        p, z = numpy.tile( numpy.roots( numpy.concatenate( ( [ 1.0 ], -self.a[ 1 : ] ) ) ), count ), numpy.tile( numpy.roots( self.b ), count )

        return p[ numpy.argsort( abs( p ) ) ], z[ numpy.argsort( abs( z ) ) ]
