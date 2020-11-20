""" **Description**

        A wavelet transform realizes a temporal spatial frequency
        transformation in the form of analysis and synthesis filters with a
        complementary frequency response, combined with downsampling and
        upsampling operations to facilitate frequency-dependent decomposition
        and reconstruction, consuming an incident signal and producing a
        reference signal.

        Analysis decomposes an incident signal into segments with specified
        operation count, applying complementary low pass and high pass analysis
        filters to an incident signal, downsampling and discarding alternate
        samples, and concatenating the paths to produce a reference signal.
        Analysis is repeated on the low pass portion of a reference signal for
        each segment, with decomposition into regions of varying temporal
        resolution, and a specific spatial frequency range.  An incident signal
        has one or two dimensions, and a length in each dimension which is
        unity or an integral multiple of 2**count.

        .. math::

            y_{i,0:\\frac{C}{2}-1} = \matrix{\downarrow(\ filter_{b_{A,L}}(\ x_{i,0:C-1}\ ),\ 2\ ) & y_{i,\\frac{C}{2}:C-1} = \downarrow(\ filter_{b_{A,H}}(\ x_{i,0:C-1}\ ),\ 2\ ) & i \in \scriptsize{[\ 0,\ R\ )}}

        .. math::

            y_{0:\\frac{R}{2}-1,j} = \matrix{\downarrow(\ filter_{b_{A,L}}(\ x_{0:R-1,j}\ ),\ 2\ ) & y_{\\frac{R}{2}:R-1,j} = \downarrow(\ filter_{b_{A,H}}(\ x_{0:R-1,j}\ ),\ 2\ ) & j \in \scriptsize{[\ 0,\ C\ )}}

        Synthesis reconstructs an incident signal from a specified operation
        count, scaling and upsampling alternate samples, applying complementary
        low pass and high pass synthesis filters to a reference signal, and
        adding the constituents to produce an incident signal.  Synthesis is
        repeated on the low pass portion of a reference signal for each segment,
        with reconstruction from regions of varying temporal resolution, and a
        specific spatial frequency range.  A reference signal has one or two
        dimensions, and a length in each dimension which is unity or an integral
        multiple of 2**count.

        .. math::

            x_{0:R-1,j} = \matrix{filter_{b_{S,L}}(\ 2\ \\uparrow(\ y_{0:\\frac{R}{2}-1,j},\ 2\ )\ ) ) + filter_{b_{S,H}}(\ 2\ \\uparrow(\ y_{\\frac{R}{2}:R-1,j},\ 2\ ) )\ ) & j \in \scriptsize{[\ 0,\ C\ )}}

        .. math::

            x_{i,0:C-1} = \matrix{filter_{b_{S,L}}(\ 2\ \\uparrow(\ y_{i,0:\\frac{C}{2}-1},\ 2\ )\ ) + filter_{b_{S,H}}(\ 2\ \\uparrow(\ y_{i,\\frac{C}{2}:C-1},\ 2\ )\ ) & i \in \scriptsize{[\ 0,\ R\ )}}

        A factory is defined to facilitate construction of an instance, defining an
        analysis filter set and a synthesis filter set of a specified order, to
        satisfy specified constraints.  An instance, classification, and order are
        specified.

        Classification is in ( 'Coiflet', 'Daubechies', 'Haar', 'Symmlet' ).

        * | 'Coiflet' is asymmetric, very high quality, with order in [ 5 : 29 : 6 ].

        * | 'Daubechies' is asymmetric, high quality, with order in [ 3 : 19 : 2 ].

        * | 'Haar' is symmetric, perfect reconstruction, with order in [ 1 ].

        * | 'Symmlet' is nearly symmetric, high quality, with order in [ 7 : 19 : 2 ].

    **Example** ::

        from diamondback import WaveletTransform
        import numpy


        count = 3

        # Create an instance from a Factory with constraints.

        obj = WaveletTransform.Factory.instance( typ = WaveletTransform, classification = 'Haar', order = 1 )

        x = numpy.random.rand( 2**( count + 3 ), 2**( count + 3 ) )

        # Transform an incident signal, forward and inverse.

        y = obj.transform( x, count, False )

        z = obj.transform( y, count, True )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-02-06.

    **Definition**

"""

from diamondback.filters.FirFilter import FirFilter
from diamondback.interfaces.IB import IB
from diamondback.interfaces.IEqual import IEqual
import numpy


class WaveletTransform( IB, IEqual ) :

    """ Wavelet transform.
    """

    class Factory( object ) :

        """ Factory.
        """

        _b = { 'Coiflet' : { 5 : numpy.array( [ -0.07269889797984, 0.33788487810742, 0.85255707635042, 0.38485416611448,
                                                -0.07272889752509, -0.01565476269428 ] ),
                             11 : numpy.array( [ 0.016387336463, -0.041464936782, -0.067372554722, 0.386110066823,
                                                 0.812723635450, 0.417005184424, -0.076488599078, -0.059434418646,
                                                 0.023680171947, 0.005611434819, -0.001823208871, -0.000720549445 ] ),
                             17 : numpy.array( [ -0.003793512864, 0.007782596426, 0.023452696142, -0.065771911281,
                                                 -0.061123390003, 0.405176902410, 0.793777222626, 0.428483476378,
                                                 -0.071799821619, -0.082301927106, 0.034555027573, 0.015880544864,
                                                 -0.009007976137, -0.002574517688, 0.001117518771, 0.000466216960,
                                                 -0.000070983303, -0.000034599773 ] ),
                             23 : numpy.array( [ 0.000892313668, -0.001629492013, -0.007346166328, 0.016068943964,
                                                 0.026682300156, -0.081266699680, -0.056077313316, 0.415308407030,
                                                 0.782238930920, 0.434386056491, -0.066627474263, -0.096220442034,
                                                 0.039334427123, 0.025082261845, -0.015211731527, -0.005658286686,
                                                 0.003751436157, 0.001266561929, -0.000589020757, -0.000259974552,
                                                 0.000062339034, 0.000031229876, -0.000003259680, -0.000001784985 ] ),
                             29 : numpy.array( [ -0.000212080863, 0.000358589677, 0.002178236305, -.004159358782,
                                                 -0.010131117538, 0.023408156762, 0.028168029062, -0.091920010549,
                                                 -0.052043163216, 0.421566206729, 0.774289603740, 0.437991626228,
                                                 -0.062035963906, -0.105574208706, 0.041289208741, 0.032683574283,
                                                 -0.019761779012, -0.009164231153, 0.006764185419, 0.002433373209,
                                                 -0.001662863769, -0.000638131296, 0.000302259520, 0.000140541149,
                                                 -0.000041340484, -0.000021315014, 0.000003734597, 0.000002063806,
                                                 -0.000000167408, -0.000000095158 ] ) },
               'Daubechies' : { 3 : numpy.array( [ 0.4829629131445341, 0.8365163037378077, 0.2241438680420134, -0.1294095225512603 ] ),
                                5 : numpy.array( [ 0.3326705529500825, 0.8068915093110924, 0.4598775021184914, -0.1350110200102546,
                                                   -0.0854412738820267, 0.0352262918857095 ] ),
                                7 : numpy.array( [ 0.2303778133088964, 0.7148465715529154, 0.6308807679398587, -0.0279837694168599,
                                                   -0.1870348117190931, 0.0308413818355607, 0.0328830116668852, -0.0105974017850690 ] ),
                                9 : numpy.array( [ 0.1601023979741929, 0.6038292697971895, 0.7243085284377726, 0.1384281459013203,
                                                   -0.2422948870663823, -0.0322448695846381, 0.0775714930400459, -0.0062414902127983,
                                                   -0.0125807519990820, 0.0033357252854738 ] ),
                                11 : numpy.array( [ 0.1115407433501095, 0.4946238903984533, 0.7511339080210959, 0.3152503517091982,
                                                    -0.2262646939654400, -0.1297668675672625, 0.0975016055873225, 0.0275228655303053,
                                                    -0.0315820393174862, 0.0005538422011614, 0.0047772575109455, -0.001073010853085 ] ),
                                13 : numpy.array( [ 0.077852054085, 0.396539319482, 0.729132090846, 0.469782287405,
                                                    -0.143906003929, -0.224036184994, 0.071309219267, 0.080612609151,
                                                    -0.038029936935, -0.016574541631, 0.012550998556, 0.000429577973,
                                                    -0.001801640704, 0.000353713800 ] ),
                                15 : numpy.array( [ 0.054415842243, 0.312871590914, 0.675630736297, 0.585354683654,
                                                    -0.015829105256, -0.284015542962, 0.000472484574, 0.128747426620,
                                                    -0.017369301002, -0.044088253931, 0.013981027917, 0.008746094047,
                                                    -0.004870352993, -0.000391740373, 0.000675449406, -0.000117476784 ] ),
                                17 : numpy.array( [ 0.038077947364, 0.243834674613, 0.604823123690, 0.657288078051,
                                                    0.133197385825, -0.293273783279, -0.096840783223, 0.148540749338,
                                                    0.030725681479, -0.067632829061, 0.000250947115, 0.022361662124,
                                                    -0.004723204758, -0.004281503682, 0.001847646883, 0.000230385764,
                                                    -0.000251963189, 0.000039347320 ] ),
                                19 : numpy.array( [ 0.026670057901, 0.188176800078, 0.527201188932, 0.688459039454,
                                                    0.281172343661, -0.249846424327, -0.195946274377, 0.127369340336,
                                                    0.093057364604, -0.071394147166, -0.029457536822, 0.033212674059,
                                                    0.003606553567, -0.010733175483, 0.001395351747, 0.001992405295,
                                                    -0.000685856695, -0.000116466855, 0.000093588670, -0.000013264203 ] ) },
               'Haar' : { 1 : numpy.array( [ 1.0, 1.0 ] ) },
               'Symmlet' : { 7 : numpy.array( [ -0.07576571478936, -0.02963552764596, 0.49761866763256, 0.80373875180539,
                                                0.29785779560561, -0.09921954357696, -0.01260396726226, 0.03222310060408 ] ),
                             9 : numpy.array( [ 0.01953888273539, -0.02110183402493, -0.17532808990810, 0.01660210576442,
                                                0.63397896345691, 0.72340769040376, 0.19939753397698, -0.03913424930258,
                                                0.02951949092607, 0.02733306834516 ] ),
                             11 : numpy.array( [ 0.01540410932734, 0.00349071208433, -0.11799011114842, -0.04831174258600,
                                                 0.49105594192767, 0.78764114102884, 0.33792942172826, -0.07263752278660,
                                                 -0.02106029251270, 0.04472490177075, 0.00176771186440, -0.00780070832477 ] ),
                             13 : numpy.array( [ 0.00268181456812, -0.00104738488897, -0.01263630340315, 0.03051551316589,
                                                 0.06789269350156, -0.04955283493702, 0.01744125508710, 0.53610191709051,
                                                 0.76776431700420, 0.28862963175084, -0.14004724044264, -0.10780823770356,
                                                 0.00401024487170, 0.01026817670849 ] ),
                             15 : numpy.array( [ 0.00188995033290, -0.00030292051455, -0.01495225833679, 0.00380875201406,
                                                 0.04913717967348, -0.02721902991682, -0.05194583810788, 0.36444189483599,
                                                 0.77718575169981, 0.48135965125924, -0.06127335906791, -0.14329423835107,
                                                 0.00760748732529, 0.03169508781035, -0.00054213233164, -0.00338241595136 ] ),
                             17 : numpy.array( [ 0.00140091552557, 0.00061978088905, -0.01327196778152, -0.01152821020798,
                                                 0.03022487885797, 0.00058346274633, -0.05456895843054, 0.23876091460724,
                                                 0.71789708276370, 0.61733844914090, 0.03527248803591, -0.19155083129635,
                                                 -0.01823377077981, 0.06207778930272, 0.00885926749351, -0.01026406402768,
                                                 -0.00047315449859, 0.00106949003265 ] ),
                             19 : numpy.array( [ 0.00077015980894, 0.00009563267076, -0.00864129927412, -0.00146538258304,
                                                 0.04592723921408, 0.01160989391052, -0.15949427882389, -0.07088053579591,
                                                 0.47169066674317, 0.76951003685204, 0.38382676114443, -0.03553674029797,
                                                 -0.03199005682142, 0.04999497206861, 0.00576491204434, -0.02035493979965,
                                                 -0.00080435893437, 0.00459317358270, 0.00005703608433, -0.00045932942045 ] ) } }

        @classmethod
        def instance( cls, typ : type, classification : str, order : int ) -> any :

            """ Constructs an instance.

                Arguments :

                    typ - Type derived from WaveletTransform ( type ).

                    classification - Classification in ( 'Coiflet', 'Daubechies', 'Haar', 'Symmlet' ) ( str ).

                    order - Order ( int ).

                Returns :

                    instance - Instance ( typ( ) ).
            """

            if ( ( not typ ) or ( not issubclass( typ, WaveletTransform ) ) ) :

                raise ValueError( 'Type = ' + str( typ ) )

            if ( classification not in WaveletTransform.Factory._b ) :

                raise ValueError( 'Classification = ' + str( classification ) )

            b = WaveletTransform.Factory._b[ classification ]

            if ( order not in b ) :

                raise ValueError( 'Order = ' + str( order ) )

            return typ( b[ order ] )

    def __init__( self, b : any ) -> None :

        """ Initialize.

            Arguments :

                b - Forward coefficient ( array( float ), list( float ) ).
        """

        if ( ( not numpy.isscalar( b ) ) and ( not isinstance( b, numpy.ndarray ) ) ) :

            b = numpy.array( list( b ) )

        if ( ( len( b.shape ) != 1 ) or ( len( b ) == 0 ) ) :

            raise ValueError( 'B = ' + str( b ) )

        super( ).__init__( )

        n = len( b ) - 1

        b = b / sum( b )

        v = numpy.flip( b, 0 )

        ii = [ 1, 1 ]

        if ( n & 1 ) :

            ii[ 1 ] = 0

        elif ( ( ( n & 3 ) == 2 ) & ( b[ : ( n // 2 ) + 1 ] == v[ : ( n // 2 ) + 1 ] ) ) :

            ii[ 0 ] = 0

        self.b = ( ( b, numpy.array( b ) ), ( v, numpy.array( v ) ) )

        for kk in range( 0, 2 ) :

            self.b[ kk ][ 1 ][ ii[ kk ] : : 2 ] *= -1.0

            if ( n != 1 ) :

                self.b[ kk ][ 1 ][ : ] = numpy.flip( self.b[ kk ][ 1 ], 0 )

    def transform( self, x : any, count : int, inverse : bool = False ) -> any :

        """ Transforms an incident signal and produces a reference signal,
            performing analysis or synthesis operations.  Incident and reference
            signals have two dimensions.  Dimension lengths must be unity or
            an integral multiple of 2**count.

            Arguments :

                x - Incident signal ( array( float ), list( float ) ).

                count - Count ( int ).

                inverse - Inverse condition ( bool ).

            Returns :

                y - Reference signal ( array( float ) ).
        """

        if ( ( not numpy.isscalar( x ) ) and ( not isinstance( x, numpy.ndarray ) ) ) :

            x = numpy.array( list( x ) )

        if ( ( len( x.shape ) > 2 ) or ( len( x ) == 0 ) ) :

            raise ValueError( 'X = ' + str( x ) )

        if ( len( x.shape ) == 2 ) :

            v = numpy.array( x )

        else :

            v = numpy.array( [ x ] )

        rows, cols = v.shape

        if ( count <= 0 ) :

            raise ValueError( 'Count = ' + str( count ) )

        if ( ( ( rows != 1 ) and ( rows % ( 2 ** count ) ) ) or ( ( cols != 1 ) and ( cols % ( 2 ** count ) ) ) ) :

            raise ValueError( '{:30s}{:30s}'.format( 'Rows = ' + str( rows ), 'Columns = ' + str( cols ) ) )

        rr = max( ( rows // ( 2 ** count ) ) * ( 2 ** count ), 1 )

        cc = max( ( cols // ( 2 ** count ) ) * ( 2 ** count ), 1 )

        y = numpy.array( v )

        b = self.b[ inverse ]

        firfilter = ( FirFilter( b[ 0 ] ), FirFilter( b[ 1 ] ) )

        if ( not inverse ) :

            if ( cc > 1 ) :

                for ii in range( 0, rr ) :

                    for kk in range( 0, 2 ) :

                        firfilter[ kk ].s[ : ] = 0.0

                        u = firfilter[ kk ].filter( v[ ii, 0 : cc ] )[ 0 ]

                        y[ ii, kk * ( cc // 2 ) : ( kk + 1 ) * ( cc // 2 ) ] = u[ 1 : : 2 ]

                v[ 0 : rr, 0 : cc ] = y[ 0 : rr, 0 : cc ]

            if ( rr > 1 ) :

                for jj in range( 0, cc ) :

                    for kk in range( 0, 2 ) :

                        firfilter[ kk ].s[ : ] = 0.0

                        u = firfilter[ kk ].filter( v[ 0 : rr, jj ] )[ 0 ]

                        y[ kk * ( rr // 2 ) : ( kk + 1 ) * ( rr // 2 ), jj ] = u[ 1 : : 2 ]

            if ( count > 1 ) :

                ii = max( rr // 2, 1 )

                jj = max( cc // 2, 1 )

                y[ 0 : ii, 0 : jj ] = self.transform( y[ 0 : ii, 0 : jj ], count - 1, inverse )

        else :

            if ( count > 1 ) :

                ii = max( rr // 2, 1 )

                jj = max( cc // 2, 1 )

                y[ 0 : ii, 0 : jj ] = self.transform( y[ 0 : ii, 0 : jj ], count - 1, inverse )

            if ( rr > 1 ) :

                u = numpy.zeros( rr )

                for jj in range( 0, cc ) :

                    w = numpy.zeros( rr )

                    for kk in range( 0, 2 ) :

                        u[ : : 2 ] = y[ kk * ( rr // 2 ) : ( kk + 1 ) * ( rr // 2 ), jj ]

                        firfilter[ kk ].s[ : ] = 0.0

                        w += 2.0 * firfilter[ kk ].filter( u )[ 0 ]

                    y[ 0 : rr, jj ] = w

            if ( cc > 1 ) :

                u = numpy.zeros( cc )

                for ii in range( 0, rr ) :

                    w = numpy.zeros( cc )

                    for kk in range( 0, 2 ) :

                        u[ : : 2 ] = y[ ii, kk * ( cc // 2 ) : ( kk + 1 ) * ( cc // 2 ) ]

                        firfilter[ kk ].s[ : ] = 0.0

                        w += 2.0 * firfilter[ kk ].filter( u )[ 0 ]

                    y[ ii, 0 : cc ] = w

        if ( len( x.shape ) == 1 ) :

            y = y[ 0 ]

        return y
