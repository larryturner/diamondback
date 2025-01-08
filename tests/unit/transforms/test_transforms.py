""" **Description**
        Test ``diamondback`` ``models``.

    **Example**

        ::

            pytest --capture=no --verbose

    **License**
        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2025 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, AI Hub, 2018-04-03.
"""

from diamondback import ComplexExponentialFilter, WindowFilter
from diamondback import ComplexTransform, FourierTransform, PsdTransform, WaveletTransform
from diamondback import ZTransform
import math
import numpy

class Test( object ) :

    """ Test.
    """

    def test_ComplexTransform( self ) :

        """ Test ComplexTransform.
        """

        count = 32
        frequency = 0.1
        x = ComplexExponentialFilter( 0.5 ).filter( numpy.linspace( -1.0e-4, 1.0e-4, count ) + frequency )
        for ii in range( 0, 2 ) :
            y = ComplexTransform.transform( x, not ii )
            assert y.shape == ( 3, count )
            assert not isinstance( y[ 0 ], complex )
            z = ComplexTransform.transform( y, not ii )
            assert z.shape == ( count, )
            assert isinstance( z[ 0 ], complex )
            assert numpy.allclose( z, x )

    def test_FourierTransform( self ) :

        """ Test FourierTransform.
        """

        count = 128
        frequency = ( 0.12, 0.23 )
        b = numpy.ones( count )
        for ii in range( 0, 4 ) :
            x = numpy.random.rand( ) * ComplexExponentialFilter( numpy.random.rand( ) ).filter( numpy.linspace( frequency[ 0 ], frequency[ 1 ], count ) )
            if ( ii % 2 ) :
                x = x.real
            if ( ii >= 2 ) :
                b = WindowFilter( 'Hann', count - 1 ).b
            y, f = FourierTransform.transform( x, b )
            assert ( ( len( y ) == count ) and ( len( f ) == count ) )
            assert isinstance( y[ 0 ], complex )
            assert numpy.isclose( f[ 0 ], -1.0 ) and numpy.isclose( f[ -1 ], 1.0 - 2.0 / count )
            h = numpy.argmax( abs( y[ count // 2 : ] ) )
            assert ( h >= numpy.argmin( abs( f[ count // 2 : ] - frequency[ 0 ] ) ) ) and ( h <= numpy.argmin( abs( f[ count // 2 : ] - frequency[ 1 ] ) ) )
            z = FourierTransform.transform( y, b, True )[ 0 ]
            if ( ii % 2 ) :
                z = z.real
            assert numpy.allclose( z[ 1 : -1 ], x[ 1 : -1 ] )

    def test_PsdTransform( self ) :

        """ Test PsdTransform.
        """

        count = 128
        frequency, index = ( 0.12, 0.23 ), 64
        b = WindowFilter( 'Hann', count - 1 ).b
        for ii in range( 0, 2 ) :
            x = numpy.random.rand( ) * ComplexExponentialFilter( numpy.random.rand( ) ).filter( numpy.linspace( frequency[ 0 ], frequency[ 1 ], count * 8 ) )
            if ( ii > 0 ) :
                x = x.real
            y, f = PsdTransform.transform( x, b, index, False )
            assert ( ( len( y ) == ( count // 2 ) ) and ( len( f ) == ( count // 2 ) ) )
            assert not isinstance( y[ 0 ], complex )
            assert numpy.isclose( f[ 0 ], 0.0 ) and numpy.isclose( f[ -1 ], 1.0 - 2.0 / count )

    def test_WaveletTransform( self ) :

        """ Test WaveletTransform.
        """

        count = 3
        h = numpy.array( [  0.235233603892082,  0.570558457915722, 0.325182500263116, -0.095467207784164,
                           -0.060416104155198, 0.024908749868442 ] )
        g = numpy.array( [ -0.024908749868442, -0.060416104155198, 0.095467207784164,  0.325182500263116,
                           -0.570558457915722, 0.235233603892082 ] )
        obj = WaveletTransform( 'Daubechies', len( h ) - 1 )
        assert numpy.allclose( obj.b[ 0 ][ 0 ], h )
        assert numpy.allclose( obj.b[ 0 ][ 1 ], g )
        h = numpy.array( [ 0.024908749868442, -0.060416104155198, -0.095467207784164, 0.325182500263116,
                           0.570558457915722,  0.235233603892082 ] )
        g = numpy.array( [ 0.235233603892082, -0.570558457915722,  0.325182500263116, 0.095467207784164,
                           -0.060416104155198, -0.024908749868442 ] )
        assert numpy.allclose( obj.b[ 1 ][ 0 ], h )
        assert numpy.allclose( obj.b[ 1 ][ 1 ], g )
        h = numpy.array( [ 0.5, 0.5 ] )
        g = numpy.array( [ 0.5, -0.5 ] )
        obj = WaveletTransform( 'Haar', len( h ) - 1 )
        assert numpy.allclose( obj.b[ 0 ][ 0 ], h )
        assert numpy.allclose( obj.b[ 0 ][ 1 ], g )
        h = numpy.array( [ 0.5, 0.5 ] )
        g = numpy.array( [ -0.5, 0.5 ] )
        assert numpy.allclose( obj.b[ 1 ][ 0 ], h )
        assert numpy.allclose( obj.b[ 1 ][ 1 ], g )
        u = numpy.array( [ -0.677118658500953,  0.345009188833763,  0.118882064536892, -0.537364409907213,
                           -0.250663848240361,  0.491955501906881, -0.545336874797487,  0.390418096834100,
                           -0.271946313073118,  0.047745751406263,  0.301454810260592,  0.138563567406933,
                           -0.215817816000671, -0.271946313073118,  0.047745751406264,  0.301454810260592,
                           -0.154508497187474, -0.110615871041237, -0.024471741852423,  0.071019760960103,
                            0.139384128958763,  0.154508497187474,  0.110615871041237,  0.024471741852423,
                           -0.071019760960103, -0.139384128958763, -0.154508497187474, -0.110615871041237,
                           -0.024471741852423,  0.071019760960104,  0.139384128958763,  0.154508497187474 ] )
        x = ComplexExponentialFilter( 0.5 ).filter( numpy.ones( len( u ) ) * 0.1 ).real
        y = obj.transform( x, count, False )
        assert numpy.allclose( y, u )
        z = obj.transform( y, count, True )
        assert numpy.allclose( z, x )
        x = numpy.zeros( ( len( u ), len( u ) ) )
        for ii in range( 0, x.shape[ 0 ] ) :
            x[ ii, : ] = numpy.random.rand( ) * ComplexExponentialFilter( numpy.random.rand( ) * 2.0 - 1.0 ).filter( numpy.ones( len( u ) ) * numpy.random.rand( ) * 0.5 ).real
        z = obj.transform( obj.transform( x, count, False ), count, True )
        assert numpy.allclose( z, x )

    def test_ZTransform( self ) :

        """ Test ZTransform.
        """

        frequency, ripple = 0.05, 0.125
        u = numpy.array( [  0.000000000000000, 1.868522837482727, -1.863713887857194, 0.948381518868702,
                           -0.212543935987133 ] )
        v = numpy.array( [ 0.016209591718306, 0.064838366873225, 0.097257550309837, 0.064838366873225,
                           0.01620959171830 ] )
        s = numpy.array( [ numpy.exp( 1j * math.pi * x / ( ( len( u ) - 1 ) * 2 ) ) for x in range( 1, ( len( u ) - 1 ) * 2, 2 ) ] )
        t = math.asinh( 1.0 / ( ( 10.0 ** ( 0.1 * ripple ) - 1.0 ) ** 0.5 ) ) / ( len( u ) - 1 )
        a = ( numpy.poly( ( -math.sinh( t ) * s.imag + 1j * math.cosh( t ) * s.real ) * 2.0 * math.pi ) ).real
        a /= a[ -1 ]
        b = [ 1.0 ]
        a, b = ZTransform.transform( a, b, frequency, True )
        b = numpy.poly( -numpy.ones( ( len( u ) - 1 ) ) )
        b *= ( 1.0 - sum( a ) ) / sum( b )
        assert numpy.allclose( a, u )
        assert numpy.allclose( b, v )
        frequency = 0.025
        u = numpy.array( [ 0.000000000000000, 4.913032434807922, -10.502699472790392, 12.647757190438988,
                           -9.256183138855487, 4.112750158020544, -1.0263940516247210, 0.110901278364195 ] )
        v = numpy.array( [ 0.000000000160721, 0.002515288055351, 0.103543670353901, 0.397913857193261,
                           0.290734727994417, 0.040371147586715, 0.000522947605366, 0.000000000000000 ] ) * 1.0e-3
        s, a = numpy.ones( 1 ), numpy.ones( 2 )
        for ii in range( 2, len( u ) ) :
            x = numpy.concatenate( ( s, numpy.zeros( 2 ) ) ) + numpy.concatenate( ( [ 0.0 ], ( ( 2.0 * ii ) - 1.0 ) * a ) )
            s, a = a, x
        a /= a[ -1 ]
        b = [ 1.0 ]
        a, b = ZTransform.transform( a, b, frequency, False )
        assert numpy.allclose( a, u )
        assert numpy.allclose( b, v )
