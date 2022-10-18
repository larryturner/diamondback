""" **Description**
        A z transform converts a continuous s-domain differential equation to a
        discrete z-domain difference equation as a function of a recursive
        coefficient array and a forward coefficient array of a specified order.
        A normalized frequency and bilinear condition are specified.

        Singleton.

        .. math::
            y_{n} = \sum_{i = 1}^{N} a_{i} y_{n-i} + \sum_{i = 0}^{N} b_{i} x_{n-i} = \sum_{i = 1}^{N} (\ a_{i} b_{0} + b_{i}\ ) s_{i,n} + b_{0} x_{n}\qquad a_{0} = 0

        A frequency response is expressed as a function of a recursive coefficient
        array and a forward coefficient array, in s-domain and z-domain.

        .. math::
            H_{s,n} = \\frac{\sum_{i = 0}^{N} v_{i} s^{N-i}}{{\sum_{i = 0}^{N} u_{i} s^{N-i}}}

        .. math::
            H_{z,n} = \\frac{\sum_{i = 0}^{N} b_{i} z^{-i}}{{1 - \sum_{i = 1}^{N} a_{i} z^{-i}}}

    **Example**
      
        ::
        
            from diamondback import ZTransform
            import math
            import numpy

            frequency, order, ripple = 0.1, 2, 0.125
            u = numpy.array( [ numpy.exp( 1j * math.pi * x / ( 2.0 * order ) ) for x in range( 1, 2 * order, 2 ) ] )
            v = math.asinh( 1.0 / ( ( 10.0 ** ( 0.1 * ripple ) - 1.0 ) ** 0.5 ) ) / order
            a = ( numpy.poly( ( -math.sinh( v ) * u.imag + 1j * math.cosh( v ) * u.real ) * 2.0 * math.pi ) ).real
            a /= a[ -1 ]

            # Transform z-domain coefficients with s-domain coefficients, frequency, and bilinear.

            a, b = ZTransform.transform( a = a, b = [ 1.0 ], frequency = frequency, bilinear = True )
            
            # Define zeros and normalize gain.

            b = numpy.poly( -numpy.ones( order ) )
            b = b * ( 1.0 - sum( a ) ) / sum( b )


    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2022 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, AI Hub, 2018-01-26.
"""

from typing import List, Tuple, Union
import math
import numpy
import scipy.signal

class ZTransform( object ) :

    """ Z transform realizes continuous s-domain to discrete z-domain transformation, through application of bilinear
        or impulse invariant methods.
    """

    @staticmethod
    def transform( u : Union[ List, numpy.ndarray ], v : Union[ List, numpy.ndarray ], frequency : float, bilinear : bool = True ) -> Tuple[ numpy.ndarray, numpy.ndarray ] :

        """ Transforms continuous s-domain coefficient arrays and produces
            discrete z-domain coefficient arrays.

            Arguments :
                u : Union[ List, numpy.ndarray ] - recursive coefficient, s-domain.
                v : Union[ List, numpy.ndarray ] - forward coefficient, s-domain.
                frequency : float - frequency in ( 0.0, inf ).
                bilinear : bool.

            Returns :
                a : numpy.ndarray - recursive coefficient, z-domain.
                b : numpy.ndarray - forward coefficient, z-domain.
        """

        if ( ( not numpy.isscalar( u ) ) and ( not isinstance( u, numpy.ndarray ) ) ) :
            u = numpy.array( list( u ) )
        if ( ( not len( u ) ) or ( not u.any( ) ) ) :
            raise ValueError( f'U = {u}' )
        if ( ( not numpy.isscalar( v ) ) and ( not isinstance( v, numpy.ndarray ) ) ) :
            v = numpy.array( list( v ) )
        if ( ( not len( v ) ) or ( not v.any( ) ) ) :
            raise ValueError( f'V = {v}' )
        if ( frequency <= 0.0 ) :
            raise ValueError( f'Frequency = {frequency} Expected Frequency in ( 0.0, inf )' )
        while ( not u[ 0 ] ) :
            u = numpy.delete( u, 0 )
        while ( not v[ 0 ] ) :
            v = numpy.delete( v, 0 )
        v /= u[ -1 ]
        u /= u[ -1 ]
        t = 1.0 / ( math.pi * frequency )
        if ( bilinear ) :
            p = numpy.roots( u )
            p = ( 1.0 + p / ( 2.0 * t ) ) / ( 1.0 - p / ( 2.0 * t ) )
            z = numpy.roots( v )
            z = ( 1.0 + z / ( 2.0 * t ) ) / ( 1.0 - z / ( 2.0 * t ) )
            if ( len( z ) < len( p ) ) :
                z = numpy.concatenate( ( z, numpy.zeros( len( p ) - len( z ) ) ) )
            a, b = numpy.poly( p ).real, numpy.poly( z ).real
        else :
            r, p, k = scipy.signal.residue( v, u )
            a, b = numpy.ones( 1 ) + 0j, 0j
            for ii in range( 0, len( r ) ) :
                a = numpy.convolve( a, numpy.array( [ 1.0, -numpy.exp( p[ ii ] / t ) ] ) )
                q = numpy.ones( 1 )
                for jj in range( 0, len( r ) ) :
                    if ( jj != ii ) :
                        q = numpy.convolve( q, numpy.array( [ 1.0, -numpy.exp( p[ jj ] / t ) ] ) )
                b += r[ ii ] * q
            if ( len( b ) < len( a ) ) :
                b = numpy.concatenate( ( b, numpy.zeros( len( a ) - len( b ) ) ) )
            a, b = a.real, b.real
        a /= -a[ 0 ]
        a[ 0 ] = 0.0
        b *= ( ( 1.0 - sum( a ) ) / sum( b ) )
        return a, b
