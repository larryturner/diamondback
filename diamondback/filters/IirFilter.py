""" **Description**

        An Infinite Impulse Response ( IIR ) filter realizes a discrete
        difference equation as a function of a recursive coefficient array,
        a forward coefficient array, and a state array of a specified order,
        consuming an incident signal and producing a reference signal.  A
        primary signal is electively specified to produce an estimation error,
        to facilitate adaptation.  A rate of adaptation is specified. ::

            y,n = sum( a,i,n * y,n-i ) + sum( b,i,n * x,n-i )  i : [ 0, N ]

                = sum( ( a,i,n * b,0,n + b,i,n ) * s,i,n ) + b,0,n * x,n

            a,0,n = 0.0

            s,1,n+1 = sum( a,i,n * s,i,n ) + x,n

            s,i,n+1 = s,i-1,n

            e,n = d,n - y,n

            q,i,n = s,i,n-1 + a,i,n-1 * q,i,n-1

            a,i,n+1 = a,i,n + rate * e,n * conjugate( b,0,n * s,i,n + a,i,n * q,i,n )

            b,i,n+1 = b,i,n + rate * e,n * conjugate( s,i,n )

        A reset may minimize edge effects at a discontinuity by assuming
        persistent operation at a specified incident signal condition. ::

            s,i,n = ( ( 1.0 - b,0,n ) / sum( a,i,n * b,0,n + b,i,n ) ) * x,n

        A frequency response is expressed as a function of a recursive
        coefficient array and a forward coefficient array. ::

            H,z,n = sum( b,i,n * z**-i ) / ( 1.0 - sum( a,i,n * z**-i ) )

        A factory is defined to facilitate construction of an instance,
        defining a recursive coefficient array, a forward coefficient array,
        and a state array of a specified order, to realize specified
        constraints.  An instance, classification, frequency, order, count,
        complement, gain, and rate are specified.

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

            from diamondback.filters.IirFilter import IirFilter
            import numpy

            obj = IirFilter.Factory.instance( typ = IirFilter, classification = 'Chebyshev', frequency = 0.1, order = 8, count = 1 )

            obj = IirFilter( a = obj.a, b = obj.b )

            y, f = obj.response( length = 8192, count = 1 )

            y, f = obj.delay( length = 8192, count = 1 )

            p, z = obj.roots( count = 1 )

            x = numpy.random.rand( 128 ) * 2.0 - 1.0

            obj.reset( x[ 0 ] )

            y = obj.filter( x )[ 0 ]

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-23.

    **Definition**

"""

from diamondback.filters.FirFilter import FirFilter
from diamondback.interfaces.IA import IA
from diamondback.interfaces.IQ import IQ
from diamondback.transforms.ZTransform import ZTransform
import math
import numpy
import scipy.signal
import warnings


class IirFilter( FirFilter, IA, IQ ) :

    """ Infinite Impulse Response ( IIR ) filter.
    """

    class Factory( object ) :

        """ Factory.
        """

        _classification = ( 'Bessel', 'Butterworth', 'Chebyshev' )

        @staticmethod
        def _evaluate( classification, frequency, order ) :

            """ Evaluates coefficients.

                Arguments :

                    classification - Classification in ( 'Bessel', 'Butterworth', 'Chebyshev' ) ( str ).

                    frequency - Normalized frequency relative to Nyquist in ( 0.0, 1.0 ) ( float ).

                    order - Order ( int ).

                Returns :

                    a - Recursive coefficient ( array( float ) ).

                    b - Forward coefficient ( array( float ) ).
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
        def instance( cls, typ, classification, frequency, order, count = 1, complement = False, gain = 1.0, rate = 0.0 ) :

            """ Constructs an instance.

                Arguments :

                    typ - Type derived from IirFilter ( type ).

                    classification - Classification in ( 'Bessel', 'Butterworth', 'Chebyshev' ) ( str ).

                    frequency - Normalized frequency relative to Nyquist in ( 0.0, 1.0 ) ( float ).

                    order - Order ( int ).

                    count - Count ( int ).

                    complement - Complement, or high pass, response condition ( bool ).

                    gain - Gain ( float ).

                    rate - Rate of adaptation in [ 0.0, 1.0 ] ( float ).

                Returns :

                    instance - Instance ( typ( ) ).
            """

            if ( ( not typ ) or ( not issubclass( typ, IirFilter ) ) ) :

                raise ValueError( 'type = ' + str( typ ) )

            if ( ( not classification ) or ( classification not in IirFilter.Factory._classification ) ) :

                raise ValueError( 'classification = ' + str( classification ) )

            if ( ( frequency <= 0.0 ) or ( frequency >= 1.0 ) ) :

                raise ValueError( 'frequency = ' + str( frequency ) )

            if ( order <= 0 ) :

                raise ValueError( 'order = ' + str( order ) )

            if ( count <= 0 ) :

                raise ValueError( 'count = ' + str( count ) )

            if ( complement ) :

                frequency = 1.0 - frequency

            beta, eps, error = 10.0, numpy.finfo( float ).eps, float( 'inf' )

            index, mu, zeta = 500 * ( 1 + ( count > 2 ) ), 2.5e-2, 1.0

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

            return typ( a, b * gain, rate = rate )

    def __init__( self, a = numpy.zeros( 1 ), b = numpy.ones( 1 ), s = numpy.zeros( 1 ), rate = 0.0 ) :

        """ Initializes an instance.

            Arguments :

                a - Recursive coefficient ( array( complex | float ), list( complex | float ) ).

                b - Forward coefficient ( array( complex | float ), list( complex | float ) ).

                s - State ( array( complex | float ), list( complex | float ) ).

                rate - Rate of adaptation in [ 0.0, 1.0 ] ( float ).
        """

        if ( ( not numpy.isscalar( a ) ) and ( not isinstance( a, numpy.ndarray ) ) ) :

            a = numpy.array( list( a ) )

        if ( ( len( a.shape ) != 1 ) or ( ( len( a ) > 0 ) and ( a[ 0 ] ) ) ) :

            raise ValueError( 'a = ' + str( a ) )

        if ( len( a ) < len( b ) ) :

            a = numpy.concatenate( ( a, numpy.zeros( len( b ) - len( a ) ) ) )

        if ( len( b ) < len( a ) ) :

            b = numpy.concatenate( ( b, numpy.zeros( len( a ) - len( b ) ) ) )

        if ( ( isinstance( a[ 0 ], complex ) ) or ( isinstance( b[ 0 ], complex ) ) ) :

            a, b = numpy.array( a, complex ), numpy.array( b, complex )

        if ( a[ 0 ] != 0.0 ) :

            raise ValueError( 'a = ' + str( a ) )

        super( ).__init__( b, s, rate )

        self.a, self.q = numpy.array( a ), numpy.array( self.s )

    def delay( self, length = 8192, count = 1 ) :

        """ Estimates group delay and produces a reference signal.

            Arguments :

                length - Length ( int ).

                count - Count ( int ).

            Returns :

                y - Reference signal ( array( float ) ).

                f - Normalized frequency relative to Nyquist in [ -1.0, 1.0 ) ( array( float ) ).
        """

        if ( length <= 0 ) :

            raise ValueError( 'length = ' + str( length ) )

        if ( count <= 0 ) :

            raise ValueError( 'count = ' + str( count ) )

        with warnings.catch_warnings( ) :

            warnings.simplefilter( 'ignore' )

            y, f = scipy.signal.group_delay( ( self.b, numpy.concatenate( ( [ 1.0 ], -self.a[ 1 : ] ) ) ), length, True )[ 1 ], numpy.linspace( -1.0, 1.0 - 2.0 / length, length )

            y = numpy.concatenate( ( y[ len( y ) // 2 : ], y[ : len( y ) // 2 ] ) )

        if ( length > 2 ) :

            y[ 0 ] = y[ 1 ] * 2.0 - y[ 2 ]

        return y, f

    def filter( self, x, d = None ) :

        """ Filters an incident signal and produces a reference signal.

            Arguments :

                x - Incident signal ( array( complex | float ), list( complex | float ) ).

                d - Primary signal ( array( complex | float ), list( complex | float ) ).

            Returns :

                y - Reference signal ( array( complex | float ) ).

                e - Error signal ( array( complex | float ) ).
        """

        if ( ( not numpy.isscalar( x ) ) and ( not isinstance( x, numpy.ndarray ) ) ) :

            x = numpy.array( list( x ) )

        if ( ( len( x.shape ) != 1 ) or ( len( x ) == 0 ) ) :

            raise ValueError( 'x = ' + str( x ) )

        y, e = numpy.zeros( len( x ), type( self.b[ 0 ] ) ), None

        if ( d is None ) :

            for ii in range( 0, len( x ) ) :

                self.s[ 0 ] = x[ ii ]

                c = self.a * self.b[ 0 ] + self.b

                y[ ii ] = c.dot( self.s )

                if ( len( self.s ) > 1 ) :

                    z = self.a.dot( self.s )

                    self.s[ 1 : ] = self.s[ : -1 ]

                    self.s[ 1 ] += z

        else :

            if ( ( not numpy.isscalar( d ) ) and ( not isinstance( d, numpy.ndarray ) ) ) :

                d = numpy.array( list( d ) )

            if ( ( len( d.shape ) != 1 ) or ( len( d ) != len( x ) ) ) :

                raise ValueError( 'd = ' + str( d ) )

            e = numpy.zeros( len( x ), type( self.b[ 0 ] ) )

            for ii in range( 0, len( x ) ) :

                self.s[ 0 ] = x[ ii ]

                c, q = self.a * self.b[ 0 ] + self.b, self.s + self.a * self.q

                y[ ii ] = c.dot( self.s )

                e[ ii ] = d[ ii ] - y[ ii ]

                self.a[ : ] += self.rate * e[ ii ] * numpy.conjugate( self.b[ 0 ] * self.s + c * self.q )

                self.b[ : ] += self.rate * e[ ii ] * numpy.conjugate( self.s )

                self.q[ : ] = q

                self.a[ 0 ], self.q[ 0 ] = 0.0, 0.0

                if ( len( self.s ) > 1 ) :

                    self.s[ 0 ] += self.a.dot( self.s )

                    self.s[ 1 : ] = self.s[ : -1 ]

                    self.s[ 0 ] = x[ ii ]

        return y, e

    def reset( self, x ) :

        """ Modifies a state to minimize edge effects by assuming persistent
            operation at a specified incident signal condition.

            Arguments :

                x - Incident signal ( complex, float ).
        """

        if ( not numpy.isscalar( x ) ) :

            raise ValueError( 'x = ' + str( x ) )

        if ( len( self.s ) > 1 ) :

            self.q.fill( 0.0 )

            self.s.fill( x * ( 1.0 - self.b[ 0 ] ) / ( self.a[ 1 : ] * self.b[ 0 ] + self.b[ 1 : ] ).sum( ) )

    def response( self, length = 8192, count = 1 ) :

        """ Estimates frequency response and produces a reference signal.

            Arguments :

                length - Length ( int ).

                count - Count ( int ).

            Returns :

                y - Reference signal ( array( complex ) ).

                f - Normalized frequency relative to Nyquist in [ -1.0, 1.0 ) ( array( float ) ).
        """

        if ( length <= 0 ) :

            raise ValueError( 'length = ' + str( length ) )

        if ( count <= 0 ) :

            raise ValueError( 'count = ' + str( count ) )

        with warnings.catch_warnings( ) :

            warnings.simplefilter( 'ignore' )

            y, f = scipy.signal.freqz( self.b, numpy.concatenate( ( [ 1.0 ], -self.a[ 1 : ] ) ), length, True )[ 1 ], numpy.linspace( -1.0, 1.0 - 2.0 / length, length )

            y = numpy.concatenate( ( y[ len( y ) // 2 : ], y[ : len( y ) // 2 ] ) ) ** count

        return y, f

    def roots( self, count = 1 ) :

        """ Estimates roots of a frequency response in poles and zeros.

            Arguments :

                count - Count.  ( int )

            Returns :

                p - Poles ( array( complex ) ).

                z - Zeros ( array( complex ) ).
        """

        p, z = numpy.tile( numpy.roots( numpy.concatenate( ( [ 1.0 ], -self.a[ 1 : ] ) ) ), count ), numpy.tile( numpy.roots( self.b ), count )

        return p[ numpy.argsort( abs( p ) ) ], z[ numpy.argsort( abs( z ) ) ]
