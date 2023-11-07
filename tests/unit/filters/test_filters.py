""" **Description**
        Test unit filters.
   
    **Example**
     
        ::
        
            pytest --capture=no --verbose
   
    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2023 Larry Turner, Schneider Electric Industries SAS. All rights reserved.
   
    **Author**
        Larry Turner, Schneider Electric, AI Hub, 2018-04-03.
"""

from diamondback import FirFilter, IirFilter, ComplexBandPassFilter, ComplexExponentialFilter
from diamondback import ComplexFrequencyFilter, DerivativeFilter, GoertzelFilter, IntegralFilter
from diamondback import PidFilter, PolynomialRateFilter, PolyphaseRateFilter, RankFilter
from diamondback import WindowFilter
import math
import numpy

class Test( object ) :

    """ Test.
    """

    def test_ComplexBandPassFilter( self ) :

        """ Test ComplexBandPassFilter.
        """

        count = 128
        frequency, rate = numpy.random.rand( ) * 2.0 - 1.0, numpy.random.rand( )
        obj = ComplexBandPassFilter( frequency, rate )
        assert numpy.isclose( obj.frequency, frequency )
        assert numpy.isclose( obj.rate, rate )
        frequency, rate = 0.1, 5.0e-2
        obj.frequency, obj.rate = frequency, rate
        assert numpy.isclose( obj.frequency, frequency )
        assert numpy.isclose( obj.rate, rate )
        x = ComplexExponentialFilter( 0.5 ).filter( numpy.linspace( -1.0e-4, 1.0e-4, count ) + frequency )
        n = ComplexExponentialFilter( 0.0 ).filter( numpy.linspace( -1.0e-4, 1.0e-4, count ) + frequency * 3.5 ) * 1.0e-3
        d = x + n
        obj.reset( d[ 0 ] )
        assert numpy.allclose( obj.s, d[ 0 ] )
        y, e, b = obj.filter( d )
        assert ( ( len( y ) == count ) and ( len( e ) == count ) and ( len( b ) == count ) )
        assert numpy.allclose( y + e, d )
        assert numpy.average( abs( e[ len( e ) - 31 : ] ) ) < 5.0e-3

    def test_ComplexExponentialFilter( self ) :

        """ Test ComplexExponentialFilter.
        """

        phase = numpy.random.rand( ) * 2.0 - 1.0
        obj = ComplexExponentialFilter( phase )
        assert numpy.isclose( obj.phase, phase )
        phase = 1.0 / 3.0
        obj.phase = phase
        assert numpy.isclose( obj.phase, phase )
        z = numpy.array( [ 0.500000000000000 + 0.866025403784439j,  0.500000000000000 + 0.866025403784439j,  0.406736643075800 + 0.913545457642601j,  0.207911690817759 + 0.978147600733806j,
                          -0.104528463267653 + 0.994521895368273j, -0.500000000000000 + 0.866025403784439j, -0.866025403784438 + 0.500000000000000j, -0.994521895368273 - 0.104528463267653j,
                          -0.669130606358858 - 0.743144825477394j,  0.104528463267653 - 0.994521895368273j,  0.866025403784438 - 0.500000000000000j,  0.866025403784439 + 0.499999999999999j,
                          -0.104528463267653 + 0.994521895368273j, -0.978147600733805 + 0.207911690817761j, -0.406736643075801 - 0.913545457642601j,  0.866025403784438 - 0.500000000000001j,
                           0.500000000000001 + 0.866025403784438j, -0.866025403784438 + 0.500000000000002j, -0.707106781186547 - 0.707106781186548j,  0.258819045102520 - 0.965925826289069j,
                           0.866025403784439 - 0.500000000000000j,  1.000000000000000 - 0.000000000000001j,  0.965925826289069 + 0.258819045102518j,  0.965925826289069 + 0.258819045102518j,
                           1.000000000000000 - 0.000000000000001j,  0.866025403784439 - 0.500000000000000j,  0.258819045102520 - 0.965925826289069j, -0.707106781186547 - 0.707106781186548j,
                          -0.866025403784438 + 0.500000000000002j,  0.500000000000001 + 0.866025403784438j,  0.707106781186547 - 0.707106781186548j, -0.965925826289068 - 0.258819045102520j ] )
        x = numpy.concatenate( ( numpy.linspace( 0.0, 0.5, len( z ) // 2 ), numpy.linspace( 0.5, -0.75, len( z ) // 2 ) ) )
        y = obj.filter( x )
        assert numpy.allclose( y, z )
        assert numpy.isclose( obj.phase, numpy.fmod( phase + sum( x ), 2.0 ) )

    def test_ComplexFrequencyFilter( self ) :

        """ Test ComplexFrequencyFilter.
        """

        count = 128
        frequency, rate = numpy.random.rand( ) * 2.0 - 1.0, numpy.random.rand( )
        obj = ComplexFrequencyFilter( frequency, rate )
        assert numpy.isclose( obj.frequency, frequency )
        assert numpy.isclose( obj.rate, rate )
        frequency, rate = 0.0, 2.0e-1
        obj.frequency, obj.rate = frequency, rate
        assert numpy.isclose( obj.frequency, frequency )
        assert numpy.isclose( obj.rate, rate )
        x = numpy.concatenate( ( numpy.linspace( 0.0, 0.05, int( count / 4 ) ), numpy.linspace( 0.05, -0.05, int( count / 2 ) ), numpy.ones( int( count / 4 ) ) * -0.05 ) )
        d = ComplexExponentialFilter( 0.0 ).filter( x )
        obj.reset( d[ 0 ] )
        y, e, b = obj.filter( d )
        assert ( ( len( y ) == count ) and ( len( e ) == count ) and ( len( b ) == count ) )
        assert abs( max( y[ int( numpy.floor( 0.25 * len( y ) ) ) : ] ) - max( x[ int( numpy.floor( 0.25 * len( x ) ) ) : ] ) ) < 5.0e-3
        assert abs( min( y[ int( numpy.floor( 0.25 * len( y ) ) ) : ] ) - min( x[ int( numpy.floor( 0.25 * len( x ) ) ) : ] ) ) < 5.0e-3
        assert abs( y[ -1 ] - x[ -1 ] ) < 5.0e-3

    def test_DerivativeFilter( self ) :

        """ Test DerivativeFilter.
        """

        count = 1024
        b, derivative = numpy.array( [ -1.0, 8.0, 0.0, -8.0, 1.0 ] ) * ( 1.0 / 12.0 ), 1
        obj = DerivativeFilter( derivative, len( b ) - 1 )
        assert numpy.allclose( obj.b, b )
        b = numpy.array( [ 1.0, -1.0 ] )
        obj = DerivativeFilter( derivative, len( b ) - 1 )
        assert numpy.allclose( obj.b, b )
        x = numpy.random.randn( count ) / 2.0
        x[ 0 ] = 0.0
        d = numpy.zeros( count )
        for ii in range( 1, count ) :
            d[ ii ] = d[ ii - 1 ] + x[ ii ]
        obj.reset( d[ 0 ] )
        assert numpy.allclose( obj.s, d[ 0 ] )
        y = obj.filter( d )
        assert numpy.allclose( y, x )

    def test_FirFilter( self ) :

        """ Test FirFilter.
        """

        b = numpy.array( [  0.00000000e+00, -4.86482301e-05, -5.14935918e-04, -1.76685187e-03,
                           -3.80954037e-03, -6.09708239e-03, -7.50679522e-03, -6.51555805e-03,
                           -1.55646139e-03,  8.52625075e-03,  2.40464408e-02,  4.41987108e-02,
                            6.70321691e-02,  8.97106501e-02,  1.09017962e-01,  1.21997354e-01,
                            1.26572673e-01,  1.21997354e-01,  1.09017962e-01,  8.97106501e-02,
                            6.70321691e-02,  4.41987108e-02,  2.40464408e-02,  8.52625075e-03,
                           -1.55646139e-03, -6.51555805e-03, -7.50679522e-03, -6.09708239e-03,
                           -3.80954037e-03, -1.76685187e-03, -5.14935918e-04, -4.86482301e-05,
                            0.00000000e+00 ] )
        obj = FirFilter( style = 'Hann', frequency = 0.1, order = len( b ) - 1, count = 1 )
        assert numpy.allclose( obj.b, b )
        b = numpy.array( [ -0.00549098, 0.00180547, 0.08123026, 0.24963445,
                            0.34564162, 0.24963445, 0.08123026, 0.00180547,
                           -0.00549098 ] )
        obj = FirFilter( style = 'Hamming', frequency = 0.25, order = len( b ) - 1, count = 1 )
        assert numpy.allclose( obj.b, b )
        obj = FirFilter( b = b, s = numpy.zeros( len( b ) ) )
        assert numpy.allclose( obj.b, b )
        obj = FirFilter( style = 'Hann', frequency = 0.2, order = 16, count = 1 )
        assert numpy.isclose( sum( obj.b ), 1.0 )
        z = numpy.array( [ 1.00000000e-01,  1.00000000e-01,  1.00421255e-01,  1.03927757e-01,
                           1.13079398e-01,  1.21006163e-01,  1.04807534e-01,  3.39511979e-02,
                          -1.09334744e-01, -3.14683417e-01, -5.45089567e-01, -7.51945156e-01,
                          -8.92849866e-01, -9.43352225e-01, -8.98263340e-01, -7.64799495e-01,
                          -5.56256475e-01, -2.92127412e-01,  5.97116498e-04,  2.92127412e-01,
                           5.55062242e-01,  7.64799495e-01,  8.99672844e-01,  9.45344165e-01,
                           8.98478611e-01,  7.64799495e-01,  5.56256475e-01,  2.92127412e-01,
                          -5.97116498e-04, -2.92127412e-01, -5.55062242e-01, -7.64799495e-01 ] )
        x = ComplexExponentialFilter( 0.5 ).filter( numpy.ones( len( z ) ) * 0.1 ).real
        n = ComplexExponentialFilter( 0.0 ).filter( numpy.ones( len( z ) ) * 0.5 ).real * 0.1
        d = x + n
        obj.reset( d[ 0 ] )
        assert numpy.allclose( obj.s, d[ 0 ] )
        y = obj.filter( d )
        assert numpy.allclose( y, z )

    def test_GoertzelFilter( self ) :

        """ Test GoertzelFilter.
        """

        count = 1024
        frequency = 0.1
        b = WindowFilter( 'Hann', count - 1 ).b
        obj = GoertzelFilter( b, frequency )
        for ii in range( 0, 4 ) :
            v = numpy.random.rand( )
            x = ComplexExponentialFilter( numpy.random.rand( ) ).filter( numpy.ones( count * 4 ) * frequency ) * v
            if ( ii % 1 ) :
                x = x.real
            y = obj.filter( x )
            assert numpy.allclose( abs( y ), v )

    def test_IirFilter( self ) :

        """ Test IirFilter.
        """

        frequency = 0.1
        a = numpy.array( [  0.000000000000000, 3.113454350028766, -4.016479371043305, 2.670363629085213,
                           -0.911373838931267, 0.127325039532952 ] )
        b = numpy.array( [ 5.221934789888007e-04, 0.002610967394944, 0.005221934789888, 0.005221934789888,
                           0.002610967394944, 5.221934789888007e-04 ] )
        obj = IirFilter( style = 'Bessel', frequency = frequency, order = len( b ) - 1, count = 1 )
        assert numpy.allclose( obj.a, a )
        assert numpy.allclose( obj.b, b )
        obj = IirFilter( a = a, b = b, s = numpy.zeros( len( a ) ) )
        assert numpy.allclose( obj.a, a )
        assert numpy.allclose( obj.b, b )
        a = numpy.array( [  0.000000000000000, 5.393212484862779, -12.147425170423173, 14.623787566618699,
                           -9.923048570780237, 3.598063533891009, -0.544601067560899 ] )
        b = numpy.array( [ 0.017536549719831, 0.105219298318984, 0.263048245797461, 0.350730994396614,
                           0.263048245797462, 0.105219298318984, 0.017536549719831 ] ) * 1.0e-5
        obj = IirFilter( style = 'Butterworth', frequency = frequency * 0.5, order = len( b ) - 1, count = 1 )
        assert numpy.allclose( obj.a, a )
        assert numpy.allclose( obj.b, b )
        z = numpy.array( [  0.100000000000000,  0.099999928272531,  0.099999044643357,  0.099993654638322,
                            0.099971704263787,  0.099903792041529,  0.099731727294888,  0.099356711892106,
                            0.098629435884824,  0.097344537593704,  0.095241822188015,  0.092015733854711,
                            0.087333189225568,  0.080858870432526,  0.072286360295633,  0.061372486218472,
                            0.047971259900082,  0.032063657922409,  0.013779991358587, -0.006587971868610,
                           -0.028587460782789, -0.051618820229716, -0.074962750944206, -0.097818954524730,
                           -0.119353657877674, -0.138752440685496, -0.155273822425082, -0.168298973582126,
                           -0.177373497823259, -0.182237747398306, -0.182842755169753, -0.179350228050951 ] )
        x = ComplexExponentialFilter( 0.5 ).filter( numpy.ones( len( z ) ) * frequency ).real
        n = ComplexExponentialFilter( 0.0 ).filter( numpy.ones( len( z ) ) * frequency * 5.0 ).real * 0.1
        d = x + n
        obj.reset( d[ 0 ] )
        s = numpy.ones( len( obj.a ) ) * 8909.962478155507
        assert len( obj.s ) == len( s )
        assert numpy.allclose( obj.s, s )
        y = obj.filter( d )
        assert numpy.allclose( y, z )
        a = numpy.array( [  0.000000000000000, 3.86461185, -5.60825317,  3.6218745,  -0.878256 ] )
        b = numpy.array( [ 1.42535217, 5.70140866, 8.55211299, 5.70140866, 1.42535217 ] ) * 1.0e-6
        obj = IirFilter( 'Chebyshev', frequency * 0.25, len( b ) - 1, 2 )
        assert numpy.allclose( obj.a, a )
        assert numpy.allclose( obj.b, b )

    def test_IntegralFilter( self ) :

        """ Test IntegralFilter.
        """

        count = 128
        a = numpy.array( [ 0.0, 1.0 , 0.0, 0.0, 0.0 ] )
        b = numpy.array( [ 7.0, 32.0, 12.0, 32.0, 7.0 ] ) * ( 1.0 / 90.0 )
        obj = IntegralFilter( len( [ x for x in b if ( not numpy.isclose( x, 0.0 ) ) ] ) - 1 )
        assert numpy.allclose( obj.a, a )
        assert numpy.allclose( obj.b, b )
        a = numpy.array( [ 0.0, 1.0 ] )
        b = numpy.array( [ 1.0, 1.0 ] ) * ( 1.0 / 2.0 )
        obj = IntegralFilter( len( [ x for x in b if ( not numpy.isclose( x, 0.0 ) ) ] ) - 1 )
        assert numpy.allclose( obj.a, a )
        assert numpy.allclose( obj.b, b )
        a = numpy.array( [ 0.0, 1.0 ] )
        b = numpy.array( [ 1.0, 0.0 ] )
        obj = IntegralFilter( len( [ x for x in b if ( not numpy.isclose( x, 0.0 ) ) ] ) - 1 )
        assert numpy.allclose( obj.a, a )
        assert numpy.allclose( obj.b, b )
        x = numpy.random.randn( count ) / 2.0
        x[ 0 ] = 0.0
        d = numpy.zeros( count )
        for ii in range( 1, count ) :
            d[ ii ] = d[ ii - 1 ] + x[ ii ]
        obj.reset( x[ 0 ] )
        assert numpy.allclose( obj.s, x[ 0 ] )
        y = obj.filter( x )
        assert numpy.allclose( y, d )

    def test_PidFilter( self ) :

        """ Test PidFilter.
        """

        count = 1024
        limit = 1.5
        b = numpy.random.randn( 3 )
        obj = PidFilter( b )
        assert numpy.allclose( obj.b, b )
        obj.limit = limit
        assert numpy.isclose( obj.limit, limit )
        obj.limit = numpy.inf
        assert numpy.isclose( obj.limit, numpy.inf )
        x = numpy.random.randn( count )
        y = obj.filter( x )
        assert len( y ) == count

    def test_PolynomialRateFilter( self ) :

        """ Test PolynomialRateFilter.
        """

        count = 32
        frequency, order = math.pi * 0.1, 3
        rate = math.pi
        r = numpy.random.rand( ) * 10.0 + 1.0
        obj = PolynomialRateFilter( r, order )
        assert numpy.isclose( obj.rate, r )
        obj.rate = rate
        assert numpy.isclose( obj.rate, rate )
        x = ComplexExponentialFilter( 0.5 ).filter( numpy.ones( count ) * frequency ).real
        y = obj.filter( x )
        z = numpy.array( [ -1.50938920e-15, -3.01286605e-01, -5.78421038e-01, -8.07251126e-01,
                           -9.35300681e-01, -9.80311079e-01, -9.44846453e-01, -7.99720095e-01,
                           -5.75258456e-01, -3.03927650e-01, -2.88149434e-03,  3.02702761e-01,
                            5.83528284e-01,  8.00381555e-01,  9.31518449e-01,  9.86496972e-01,
                            9.45905739e-01,  7.93857933e-01,  5.76364443e-01,  3.09155188e-01,
                            1.97908969e-03, -3.06078665e-01, -5.87611199e-01, -7.93455291e-01,
                           -9.33972480e-01, -9.97190305e-01, -9.36926168e-01, -7.92272692e-01,
                           -5.82874118e-01, -3.07568750e-01,  7.84550105e-04,  3.08790848e-01,
                            5.78688584e-01,  7.92470898e-01,  9.41440696e-01,  9.91029455e-01,
                            9.31913194e-01,  7.96464675e-01,  5.85774047e-01,  3.04173769e-01,
                           -2.84387507e-03, -3.06800272e-01, -5.75134650e-01, -7.96631541e-01,
                           -9.50649339e-01, -9.82462303e-01, -9.32768893e-01, -8.06310373e-01,
                           -5.80702911e-01, -3.01540819e-01,  1.87274326e-03,  3.01915167e-01,
                            5.76559550e-01,  8.03758347e-01,  9.39084678e-01,  9.79501593e-01,
                            9.39826199e-01,  8.03169181e-01,  5.76308538e-01,  3.02115621e-01,
                            2.09267642e-03, -3.01656744e-01, -5.81104941e-01, -8.05385284e-01,
                           -9.32476390e-01, -9.82943717e-01, -9.50588784e-01, -7.96171920e-01,
                           -5.75215932e-01, -3.07380275e-01, -2.76802714e-03,  3.04442192e-01,
                            5.86112809e-01,  7.95928727e-01,  9.32106032e-01,  9.91862011e-01,
                            9.40740088e-01,  7.92343961e-01,  5.79191217e-01,  3.08662743e-01,
                            5.63419210e-04, -3.07784965e-01, -5.82182945e-01, -7.92199630e-01,
                           -9.37509152e-01, -9.96269822e-01, -9.33580539e-01, -7.93778141e-01,
                           -5.87588041e-01, -3.05808939e-01,  2.14525625e-03,  3.09141999e-01,
                            5.76092393e-01,  7.94185235e-01,  9.46680110e-01,  9.61139947e-01,
                            8.89551638e-01,  7.78862770e-01,  6.84415649e-01,  6.07716745e-01,
                            5.31017840e-01 ] )
        assert numpy.allclose( y, z )

    def test_PolyphaseRateFilter( self ) :

        """ Test PolyphaseRateFilter.
        """

        count = 128
        frequency, rate = math.pi * 0.1, math.pi
        polyphaseratefilter = PolyphaseRateFilter( 0.1 )
        assert numpy.isclose( polyphaseratefilter.rate, 0.1 )
        polyphaseratefilter.rate = rate
        assert numpy.isclose( polyphaseratefilter.rate, rate )
        x = ComplexExponentialFilter( 0.5 ).filter( numpy.ones( count ) * frequency ).real
        polyphaseratefilter.reset( x[ 0 ] )
        assert numpy.allclose( polyphaseratefilter.s, x[ 0 ] )
        y = polyphaseratefilter.filter( x )
        assert numpy.isclose( len( y ), numpy.floor( count * rate ) ) or numpy.isclose( len( y ), numpy.ceil( count * rate ) )
        rate, count = 1.0 / rate, len( y )
        polyphaseratefilter.rate = rate
        polyphaseratefilter.reset( y[ 0 ] )
        z = polyphaseratefilter.filter( y )
        assert numpy.isclose( len( z ), numpy.floor( count * rate ) ) or numpy.isclose( len( z ), numpy.ceil( count * rate ) )
        rate, count = 0.25, 64
        x = numpy.concatenate( ( numpy.linspace( -1.0, 1.0, count // 2 ), numpy.linspace( 1.0, -1.0, count // 2 ) ) )
        polyphaseratefilter.rate = rate
        polyphaseratefilter.reset( 0.0 )
        y = polyphaseratefilter.filter( x )
        z = numpy.array( [  0.00000000,  0.02061912, -1.09636725, -0.71004968,
                           -0.45148771, -0.19342319,  0.06464132,  0.32270584,
                            0.58077036,  0.83952135,  0.97098504,  0.70966357,
                            0.45148771,  0.19342319, -0.06464132, -0.32270584 ] )
        assert numpy.allclose( y, z )

    def test_RankFilter( self ) :

        """ Test RankFilter.
        """

        index, order = 4, 4
        obj = RankFilter( index, order )
        assert obj.index == index
        assert len( obj.s ) == order + 1
        x = numpy.concatenate( ( numpy.ones( 1 ), numpy.zeros( 15 ), numpy.ones( 4 ), numpy.zeros( 2 ), numpy.ones( 5 ), numpy.zeros( 6 ) ) )
        obj.reset( x[ 0 ] )
        assert numpy.allclose( obj.s, x[ 0 ] )
        y = obj.filter( x )
        z = numpy.concatenate( ( numpy.ones( 5 ), numpy.zeros( 11 ), numpy.ones( 15 ), numpy.zeros( 2 ) ) )
        assert numpy.allclose( y, z )

    def test_WindowFilter( self ) :

        """ Test WindowFilter.
        """

        b = numpy.array( [ 0.00000000, 0.04322727, 0.16543470, 0.34549150,
                           0.55226423, 0.75000000, 0.90450850, 0.98907380,
                           0.98907380, 0.90450850, 0.75000000, 0.55226423,
                           0.34549150, 0.16543470, 0.04322727, 0.00000000 ] )
        obj = WindowFilter( 'Hann', len( b ) - 1, False )
        assert numpy.allclose( obj.b, b )
        obj = WindowFilter( 'Hann', len( b ) - 1, True )
        assert numpy.allclose( obj.b, b * len( b ) / sum( abs( b ) ) )
