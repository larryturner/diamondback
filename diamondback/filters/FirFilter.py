""" **Description**

        A Finite Impulse Response ( FIR ) filter realizes a discrete difference
        equation as a function of a forward coefficient array and a state array
        of a specified order, consuming an incident signal and producing a
        reference signal.

        .. math::

            y_{n} = \sum_{i = 0}^{N} b_{i,n} x_{n-i} = \sum_{i = 1}^{N} b_{i,n} s_{i,n} + b_{0,n} x_{n}

        .. math::

            s_{1,n+1} = x_{n}\qquad\quad s_{i,n+1} = s_{i-1,n}

        A reset may minimize edge effects at a discontinuity by assuming
        persistent operation at a specified incident signal condition.

        .. math::

            s_{i,n} = x_{n}

        A frequency response is expressed as a function of a forward
        coefficient array.

        .. math::

            H_{z,n} = \sum_{i = 0}^{N} b_{i,n} z^{-i}

        A factory is defined to facilitate construction of an instance,
        defining a forward coefficient array, and a state array of a
        specified order, to realize specified constraints.  An instance,
        classification, frequency, order, count, complement, and gain
        are specified.

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

            from diamondback import FirFilter
            import numpy

            # Create an instance from a Factory with constraints.

            obj = FirFilter.Factory.instance( typ = FirFilter, classification = 'Kaiser', frequency = 0.1, order = 32, count = 1 )

            # Create an instance with coefficients.

            obj = FirFilter( b = obj.b )

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

from diamondback.interfaces.IB import IB
from diamondback.interfaces.IReset import IReset
from diamondback.interfaces.IS import IS
from typing import Any, List, Tuple, Union
import math
import numpy
import scipy.signal
import warnings

class FirFilter( IB, IReset, IS ) :

    """ Finite Impulse Response ( FIR ) filter.
    """

    class Factory( object ) :

        """ Factory.
        """

        _classification = ( 'Blackman', 'Hamming', 'Hann', 'Kaiser' )

        @classmethod
        def instance( cls, typ : type, classification : str, frequency : float, order : int, count : int = 1, complement : bool = False, gain : float = 1.0 ) -> Any :

            """ Constructs an instance.

                Arguments :

                    typ : type - derived from FirFilter.

                    classification : str - in ( 'Blackman', 'Hamming', 'Hann', 'Kaiser' ).

                    frequency : float - relative to Nyquist in ( 0.0, 1.0 ).

                    order : int.

                    count : int.

                    complement : bool.

                    gain : float.

                Returns :

                    instance : typ( ).
            """

            if ( ( not typ ) or ( not issubclass( typ, FirFilter ) ) ) :

                raise ValueError( f'Type = {typ}' )

            if ( ( not classification ) or ( classification not in FirFilter.Factory._classification ) ) :

                raise ValueError( f'Classification = {classification}' )

            if ( ( frequency <= 0.0 ) or ( frequency >= 1.0 ) ) :

                raise ValueError( f'Frequency = {frequency}' )

            if ( order < 0 ) :

                raise ValueError( f'Order = {order}' )

            if ( count <= 0 ) :

                raise ValueError( f'Count = {count}' )

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

                        raise ValueError( f'V = {v}' )

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

            return typ( b * gain )

    def __init__( self, b : Union[ List, numpy.ndarray ] = numpy.ones( 1 ), s : Union[ List, numpy.ndarray ] = numpy.zeros( 1 ) ) -> None :

        """ Initialize.

            Arguments :

                b : Union[ List, numpy.ndarray ] - forward coefficient.

                s : Union[ List, numpy.ndarray ] - state.
        """

        if ( ( not numpy.isscalar( b ) ) and ( not isinstance( b, numpy.ndarray ) ) ) :

            b = numpy.array( list( b ) )

        if ( ( len( b.shape ) != 1 ) or ( len( b ) == 0 ) ) :

            raise ValueError( f'B = {b}' )

        if ( ( not numpy.isscalar( s ) ) and ( not isinstance( s, numpy.ndarray ) ) ) :

            s = numpy.array( list( s ) )

        if ( ( len( s.shape ) != 1 ) or ( len( s ) == 0 ) ) :

            raise ValueError( f'S = {s}' )

        if ( len( b ) < len( s ) ) :

            b = numpy.concatenate( ( b, numpy.zeros( len( s ) - len( b ) ) ) )

        if ( len( s ) < len( b ) ) :

            s = numpy.concatenate( ( s, numpy.zeros( len( b ) - len( s ) ) ) )

        super( ).__init__( )

        self.b, self.s = numpy.array( b ), numpy.array( s, type( b[ 0 ] ) )

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

            y, f = scipy.signal.group_delay( ( self.b, [ 1.0 ] ), length, True )[ 1 ], numpy.linspace( -1.0, 1.0 - 2.0 / length, length )

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

            y[ ii ] = self.b.dot( self.s )

            if ( len( self.s ) > 1 ) :

                self.s[ 1 : ] = self.s[ : -1 ]

        return y

    def reset( self, x : Union[ complex, float ] ) -> None :

        """ Modifies a state to minimize edge effects by assuming persistent
            operation at a specified incident signal condition.

            Arguments :

                x : Union[ complex, float ] - incident signal.
        """

        if ( not numpy.isscalar( x ) ) :

            raise ValueError( f'X = {x}' )

        self.s.fill( x )

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

        y, f = scipy.signal.freqz( self.b, [ 1.0, 0.0 ], length, True )[ 1 ], numpy.linspace( -1.0, 1.0 - 2.0 / length, length )

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

        z = numpy.tile( numpy.roots( self.b ), count )

        return numpy.zeros( count * ( len( self.b ) - 1 ) ), z[ numpy.argsort( abs( z ) ) ]
