""" **Description**

        Test unit models.

    **Example**

        ::

            pytest --capture=no --verbose

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-04-03.

    **Definition**

"""

from diamondback import DiversityModel, PrincipalComponentModel
import numpy

class Test( object ) :

    """ Test.
    """

    def test_DiversityModel( self ) :

        """ Test DiversityModel.
        """

        ii = [ 11, 1, 2, 3, 10 ]

        obj = DiversityModel.Factory.instance( DiversityModel, 'Euclidean', len( ii ) - 1 )

        assert obj.s.shape == ( 0, len( ii ) )

        x = numpy.transpose( numpy.array( [ [ 0.929263623187228, 0.349983765984809 ],
                                            [ 0.232958886794845, 0.323811130703304 ],
                                            [ 0.688771948873912, 0.618743394357275 ],
                                            [ 0.460750416153906, 1.049010446078109 ],
                                            [ 0.730718636607270, 0.840632699200231 ],
                                            [ 1.099011845647992, 0.649475382456737 ],
                                            [ 0.975382047292540, 1.190092730642132 ],
                                            [ 0.634991301520811, 1.076912549816130 ],
                                            [ 0.366763380472155, 0.635768300484789 ],
                                            [ 0.858070280281700, 1.433712684647466 ],
                                            [ 1.297647047865546, 0.857178935746457 ],
                                            [ 0.968823660872193, 1.269390641058206 ] ] ) )

        y = obj.model( x )

        v = numpy.array( [ 0.000000, 0.000000, 0.000000, 0.000000,
                           0.000000, 0.344252, 0.411389, 0.411389,
                           0.411389, 0.411389, 0.463343, 0.486953 ] )

        s = x[ :, ii ]

        assert numpy.allclose( y, v )

        assert numpy.allclose( s, obj.s )

    def test_PrincipalComponentModel( self ) :

        """ Test PrincipalComponentModel.
        """

        obj = PrincipalComponentModel( )

        x = numpy.array( [ [  0.92982611,  1.15628026,  1.32456014,  1.54128238,
                              1.74483926,  1.96410142,  2.1236406,   2.33322998,
                              2.54608544,  2.72938233,  2.94649129,  3.12654834,
                              3.32354533,  3.53998025,  3.74830022,  3.93698861,
                              4.12628495,  4.3308249,   4.51245397,  4.73479443,
                              4.93920801,  5.11598669,  5.33570473,  0.24212283,
                              0.22012508,  0.14934957,  0.97633905,  0.97096045,
                              0.95997718,  0.93026206,  0.9568895,   0.95602598 ],
                           [ -0.3244762,  -0.71636682,  0.7953886,   0.56577115,
                              1.92561563,  3.00823443, -1.31038351,  2.23158514,
                             -1.00787509,  2.93960357,  2.35920054, -1.26451386,
                              3.40962949,  1.54696917,  1.16923639, -0.67688605,
                             -1.72410373,  2.46323018, -0.69589292,  2.71666323,
                             -2.23920976,  1.47586666, -0.5732845,   1.34003134,
                              0.16294568,  -0.1724991,  1.91744129, -3.04463511,
                              1.7101014,  -0.21883699, -0.79983005, -0.98445655 ],
                           [  2.09311328,  1.94350435,  1.6062583,   1.24822057,
                              1.06441375,  0.51440064,  0.80396202,  0.2596621,
                              0.31071599,  0.14704657, -0.29802407, -0.44813363,
                             -0.95537275, -1.1734108,  -1.27433861, -1.73554431,
                             -1.61246782, -1.96325253, -2.10754974, -2.64582438,
                             -3.08695416, -3.17924651, -3.41005082,  3.27276207,
                              3.62380914,  3.97015509,  1.17915077,  1.19028501,
                              0.85939319,  1.07123524,  0.8553237,   0.95840126 ] ] )

        y = obj.model( x )

        assert x.shape == y.shape

        z = numpy.array( [ [ -1.45997195e+00, -1.32375611e+00, -1.04601052e+00, -8.28882785e-01,
                             -5.99805998e-01, -2.42945473e-01, -5.01485839e-01, -2.40198010e-02,
                             -1.14995160e-01,  2.31258393e-01,  4.62542402e-01,  4.11252232e-01,
                              9.27899314e-01,  1.00890223e+00,  1.11978280e+00,  1.27892708e+00,
                              1.26409036e+00,  1.70125405e+00,  1.67252159e+00,  2.14678274e+00,
                              2.14491886e+00,  2.44992410e+00,  2.52747102e+00, -2.11667249e+00,
                             -2.31680167e+00, -2.49353563e+00, -9.86235666e-01, -1.24906616e+00,
                             -8.86316128e-01, -1.07738618e+00, -1.01584743e+00, -1.06379217e+00 ],
                           [  6.38250518e-02,  1.13859607e-01,  4.99707411e-02,  1.69134354e-02,
                              2.71252606e-02, -8.85097181e-02,  1.31921079e-01, -9.64696162e-03,
                              1.36017321e-01,  1.19647342e-01,  5.79256877e-02,  1.18102718e-01,
                             -2.63109425e-02,  8.07163699e-03,  6.78519538e-02, -3.98418244e-04,
                              1.40222308e-01,  6.18056136e-02,  1.20361578e-01, -1.20052778e-02,
                             -3.57895523e-02, -2.64214261e-02,  6.50637684e-03,  1.75813272e-01,
                              3.07242495e-01,  4.06925103e-01, -2.75254313e-01, -2.25715402e-01,
                             -3.98972643e-01, -3.15293111e-01, -3.77670926e-01, -3.38119889e-01 ],
                           [ -3.66924042e-01, -6.13152330e-01,  2.69124588e-01,  1.11935139e-01,
                              9.08450986e-01,  1.52544854e+00, -1.04072111e+00,  1.04157009e+00,
                             -8.92600547e-01,  1.44649581e+00,  1.07706296e+00, -1.09257365e+00,
                              1.66583757e+00,  5.41345739e-01,  3.05970433e-01, -8.17033093e-01,
                             -1.44204099e+00,  1.03213470e+00, -8.60623338e-01,  1.14441758e+00,
                             -1.83046498e+00,  3.73130777e-01, -8.63022097e-01,  6.90929543e-01,
                              3.89264228e-03, -1.80509749e-01,  9.32165457e-01, -2.02262041e+00,
                              7.97045750e-01, -3.42833551e-01, -6.97909272e-01, -8.03929143e-01 ] ] )

        assert numpy.allclose( y, z )

        e = numpy.array( [ 1.97348626, 0.03358314, 0.99293059 ] )

        v = numpy.array( [ [  0.70495169,  0.08639378, -0.70397389 ],
                           [  0.70751261, -0.01612183,  0.7065168 ],
                           [ -0.04968931,  0.99613061,  0.0724898 ] ] )

        assert numpy.allclose( e, obj.e )

        assert numpy.allclose( v, obj.v )
