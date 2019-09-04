""" **Description**

        A Finite Impulse Response ( FIR ) filter realizes a discrete difference
        equation as a function of a forward coefficient array and a state array
        of a specified order, consuming an incident signal and producing a
        reference signal.  A primary signal is electively specified to produce
        an estimation error, to facilitate adaptation.  A rate of adaptation is
        specified. ::

            y,n = sum( b,i,n * x,n-i )                         i : [ 0, N ]

                = sum( b,i,n * s,i,n ) + b,0,n * x,n

            s,1,n+1 = x,n

            s,i,n+1 = s,i-1,n

            e,n = d,n - y,n

            b,i,n+1 = b,i,n + rate * e,n * conjugate( s,i,n )

        A reset may minimize edge effects at a discontinuity by assuming
        persistent operation at a specified incident signal condition. ::

            s,i,n = x,n

        A frequency response is expressed as a function of a forward
        coefficient array. ::

            H,z,n = sum( b,i,n * z**-i )

        A factory is defined to facilitate construction of an instance,
        defining a forward coefficient array, and a state array of a
        specified order, to realize specified constraints.  An instance,
        classification, frequency, order, count, complement, gain, and
        rate are specified.

        Frequency corresponds to a -3 dB frequency response normalized relative
        to Nyquist.

        Classification is in ( 'Blackman', 'Hamming', 'Hann', 'Kaiser' ).

        * | 'Blackman' filters demonstrate low resolution and spectral leakage
          | with improved rate of attenuation.

        * | 'Hamming' filters demonstrate minimal nearest side lobe magnitude
          | response.

        * | 'Hann' filters demonstrate high resolution and spectral leakage.

        * | 'Kaiser' filters demonstrate flexible resolution and spectral
          | leakage dependent upon a beta value of a Bessel function of the
          | first kind, with beta equal to 7.0.

        Order must even to ensure a Type I form linear phase solution.

        Count is a quantity of filters of a specified order concatenated to
        form an aggregate frequency response in cascade form.

        Complement effectively constructs a mirror image of a specified
        frequency response.

    **Example**

        ::

            from diamondback.filters.FirFilter import FirFilter
            import numpy

            obj = FirFilter.Factory.instance( typ = FirFilter, classification = 'Kaiser', frequency = 0.1, order = 32, count = 1 )

            obj = FirFilter( b = obj.b )

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

from diamondback.interfaces.IB import IB
from diamondback.interfaces.IRate import IRate
from diamondback.interfaces.IReset import IReset
from diamondback.interfaces.IS import IS
import math
import numpy
import scipy.signal
import warnings


class FirFilter( IB, IRate, IReset, IS ) :

    """ Finite Impulse Response ( FIR ) filter.
    """

    class Factory( object ) :

        """ Factory.
        """

        _classification = ( 'Blackman', 'Hamming', 'Hann', 'Kaiser' )

        @classmethod
        def instance( cls, typ, classification, frequency, order, count = 1, complement = False, gain = 1.0, rate = 0.0 ) :

            """ Constructs an instance.

                Arguments :

                    typ - Type derived from FirFilter ( type ).

                    classification - Classification in ( 'Blackman', 'Hamming', 'Hann', 'Kaiser' ) ( str ).

                    frequency - Normalized frequency relative to Nyquist in ( 0.0, 1.0 ) ( float ).

                    order - Order ( int ).

                    count - Count ( int ).

                    complement - Complement, or high pass, response condition ( bool ).

                    gain - Gain ( float ).

                    rate - Rate of adaptation in [ 0.0, 1.0 ] ( float ).

                Returns :

                    instance - Instance ( typ( ) ).
            """

            if ( ( not typ ) or ( not issubclass( typ, FirFilter ) ) ) :

                raise ValueError( 'type = ' + str( typ ) )

            if ( ( not classification ) or ( classification not in FirFilter.Factory._classification ) ) :

                raise ValueError( 'classification = ' + str( classification ) )

            if ( ( frequency <= 0.0 ) or ( frequency >= 1.0 ) ) :

                raise ValueError( 'frequency = ' + str( frequency ) )

            if ( order < 0 ) :

                raise ValueError( 'order = ' + str( order ) )

            if ( count <= 0 ) :

                raise ValueError( 'count = ' + str( count ) )

            if ( complement ) :

                frequency = 1.0 - frequency

            if ( classification == 'Kaiser' ) :

                window = ( classification.lower( ), 7.0 )

            else :

                window = classification.lower( )

            beta, eps, error = 10.0, numpy.finfo( float ).eps, float( 'inf' )

            index, mu, zeta = 500 * ( 1 + ( count > 2 ) ), 2.5e-2, 1.0

            for ii in range( 0, index ) :

                with warnings.catch_warnings( ) :

                    warnings.simplefilter( 'ignore' )

                    v = scipy.signal.firwin( order + 1, zeta * frequency, None, window, True, True, 1.0 )

                    if ( numpy.isnan( v ).any( ) ) :

                        raise ValueError( 'b = ' + str( v ) )

                    x = numpy.exp( 1j * math.pi * frequency )

                    e = ( 2.0 ** ( -0.5 ) ) - ( abs( numpy.polyval( v, x ) ) ** count )

                    if ( abs( e ) < error ) :

                        b, error = v, abs( e )

                        if ( error < ( 10.0 * eps ) ) :

                            break

                    zeta = numpy.maximum( zeta + mu * math.tanh( beta * e ), eps )

            if ( complement ) :

                b *= numpy.array( [ ( ( -1.0 ) ** x ) for x in range( 0, len( b ) ) ] )

                b /= sum( b * numpy.array( [ ( ( -1.0 ) ** x ) for x in range( 0, len( b ) ) ] ) )

            return typ( b * gain, rate = rate )

    def __init__( self, b = numpy.ones( 1 ), s = numpy.zeros( 1 ), rate = 0.0 ) :

        """ Initializes an instance.

            Arguments :

                b - Forward coefficient ( array( complex | float ), list( complex | float ) ).

                s - State ( array( complex | float ), list( complex | float ) ).

                rate - Rate of adaptation in [ 0.0, 1.0 ] ( float ).
        """

        if ( ( not numpy.isscalar( b ) ) and ( not isinstance( b, numpy.ndarray ) ) ) :

            b = numpy.array( list( b ) )

        if ( ( len( b.shape ) != 1 ) or ( len( b ) == 0 ) ) :

            raise ValueError( 'b = ' + str( b ) )

        if ( ( not numpy.isscalar( s ) ) and ( not isinstance( s, numpy.ndarray ) ) ) :

            s = numpy.array( list( s ) )

        if ( ( len( s.shape ) != 1 ) or ( len( s ) == 0 ) ) :

            raise ValueError( 's = ' + str( s ) )

        if ( len( b ) < len( s ) ) :

            b = numpy.concatenate( ( b, numpy.zeros( len( s ) - len( b ) ) ) )

        if ( len( s ) < len( b ) ) :

            s = numpy.concatenate( ( s, numpy.zeros( len( b ) - len( s ) ) ) )

        super( ).__init__( )

        self.b, self.s = numpy.array( b ), numpy.array( s, type( b[ 0 ] ) )

        self.rate = rate

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

            y, f = scipy.signal.group_delay( ( self.b, [ 1.0 ] ), length, True )[ 1 ], numpy.linspace( -1.0, 1.0 - 2.0 / length, length )

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

                y[ ii ] = self.b.dot( self.s )

                if ( len( self.s ) > 1 ) :

                    self.s[ 1 : ] = self.s[ : -1 ]

        else :

            if ( ( not numpy.isscalar( d ) ) and ( not isinstance( d, numpy.ndarray ) ) ) :

                d = numpy.array( list( d ) )

            if ( ( len( d.shape ) != 1 ) or ( len( d ) != len( x ) ) ) :

                raise ValueError( 'd = ' + str( d ) )

            e = numpy.zeros( len( x ), type( self.b[ 0 ] ) )

            for ii in range( 0, len( x ) ) :

                self.s[ 0 ] = x[ ii ]

                y[ ii ] = self.b.dot( self.s )

                e[ ii ] = d[ ii ] - y[ ii ]

                self.b[ : ] += self.rate * e[ ii ] * numpy.conjugate( self.s )

                if ( len( self.s ) > 1 ) :

                    self.s[ 1 : ] = self.s[ : -1 ]

        return y, e

    def reset( self, x ) :

        """ Modifies a state to minimize edge effects by assuming persistent
            operation at a specified incident signal condition.

            Arguments :

                x - Incident signal ( complex, float ).
        """

        if ( not numpy.isscalar( x ) ) :

            raise ValueError( 'x = ' + str( x ) )

        self.s.fill( x )

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

        y, f = scipy.signal.freqz( self.b, [ 1.0, 0.0 ], length, True )[ 1 ], numpy.linspace( -1.0, 1.0 - 2.0 / length, length )

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

        z = numpy.tile( numpy.roots( self.b ), count )

        return numpy.zeros( count * ( len( self.b ) - 1 ) ), z[ numpy.argsort( abs( z ) ) ]
