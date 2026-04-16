"""**Description**
    Test.

**Example**

    ::

        pytest --capture=no --verbose

**License**
    `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
    © 2018 - 2026 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

**Author**
    Larry Turner, Schneider Electric, AI Hub, 2018-04-03.
"""

import numpy

from diamondback import ComplexExponentialFilter, IirFilter


class TestIirFilter(object):
    """Test IirFilter."""

    def test_init(self):
        """Test init."""

        a = numpy.array([0.0000000000, 3.11345435, -4.016479371, 2.670363629, -0.9113738389, 0.1273250395])
        b = numpy.array([0.0005221935, 0.0026109674, 0.0052219348, 0.0052219348, 0.0026109674, 0.0005221935])
        iir_filter = IirFilter(style="Bessel", frequency=0.1, order=len(b) - 1, count=1)
        assert numpy.allclose(iir_filter.a, a)
        assert numpy.allclose(iir_filter.b, b)
        iir_filter = IirFilter(a=a, b=b, s=numpy.zeros(len(a)))
        assert numpy.allclose(iir_filter.a, a)
        assert numpy.allclose(iir_filter.b, b)
        a = numpy.array(
            [0.0000000000, 5.3932124849, -12.1474251704, 14.6237875666, -9.9230485708, 3.5980635339, -0.5446010676]
        )
        b = numpy.array(
            [
                1.7536549721e-07,
                1.0521929832e-06,
                2.6304824581e-06,
                3.5073099441e-06,
                2.6304824581e-06,
                1.0521929832e-06,
                1.7536549721e-07,
            ]
        )
        iir_filter = IirFilter(style="Butterworth", frequency=0.05, order=len(b) - 1, count=1)
        assert numpy.allclose(iir_filter.a, a)
        assert numpy.allclose(iir_filter.b, b)
        assert numpy.allclose(iir_filter.s, 0.0)
        z = numpy.array(
            [
                1.753654971914e-08,
                1.456067183425e-07,
                3.895529756880e-07,
                -7.390432379724e-07,
                -1.039304228348e-05,
                -4.907830466681e-05,
                -1.610293252688e-04,
                -4.253892439800e-04,
                -9.659936397280e-04,
                -1.957319287929e-03,
                -3.624159774970e-03,
                -6.233451546404e-03,
                -1.007803925531e-02,
                -1.545316856035e-02,
                -2.262720984575e-02,
                -3.180913888176e-02,
                -4.311629168853e-02,
                -5.654606814920e-02,
                -7.195477308227e-02,
                -8.904638597528e-02,
                -1.073735611528e-01,
                -1.263519372073e-01,
                -1.452872172607e-01,
                -1.634133228871e-01,
                -1.799391268515e-01,
                -1.941002279746e-01,
                -2.052112711932e-01,
                -2.127142284713e-01,
            ]
        )
        x = ComplexExponentialFilter(0.5).filter(numpy.ones(len(z)) * 0.1).real
        n = ComplexExponentialFilter(0.0).filter(numpy.ones(len(z)) * 0.5).real * 0.1
        d = x + n
        y = iir_filter.filter(d)
        assert numpy.allclose(y, z)
        iir_filter.reset(d[0])
        s = numpy.ones(len(iir_filter.a)) * 8909.962478155508
        s[0] = d[0]
        assert numpy.allclose(s, iir_filter.s)
        z = numpy.array(
            [
                0.100000000000,
                0.099999928273,
                0.099999044643,
                0.099993654638,
                0.099971704264,
                0.099903792042,
                0.099731727295,
                0.099356711892,
                0.098629435885,
                0.097344537594,
                0.095241822188,
                0.092015733855,
                0.087333189226,
                0.080858870433,
                0.072286360297,
                0.06137248622,
                0.047971259902,
                0.032063657924,
                0.01377999136,
                -0.006587971867,
                -0.028587460781,
                -0.051618820228,
                -0.074962750943,
                -0.097818954524,
                -0.119353657877,
                -0.138752440686,
                -0.155273822427,
                -0.168298973585,
            ]
        )
        y = iir_filter.filter(d)
        assert numpy.allclose(y, z)
        a = numpy.array([0.0000000000, 3.8765072084, -5.6415809915, 3.653029515, -0.8879718207])
        b = numpy.array([1.0055554834e-06, 4.0222219335e-06, 6.0333329003e-06, 4.0222219335e-06, 1.0055554834e-06])
        iir_filter = IirFilter(style="Chebyshev", frequency=0.025, order=len(b) - 1, count=2)
        assert numpy.allclose(iir_filter.a, a)
        assert numpy.allclose(iir_filter.b, b)
