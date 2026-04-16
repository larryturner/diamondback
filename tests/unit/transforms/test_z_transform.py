"""**Description**
    Test.

**Example**

    ::

        pytest --capture=no --verbose

**License**
    `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_
    © 2018 - 2026 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

**Author**
    Larry Turner, Schneider Electric, AI Hub, 2018-04-03.
"""

import math

import numpy

from diamondback import ZTransform


class TestZTransform(object):
    """Test ZTransform."""

    def test_init(self):
        """Test init."""

        frequency, ripple = 0.05, 0.125
        u = numpy.array(
            [
                0.000000000000000,
                1.868522837482727,
                -1.863713887857194,
                0.948381518868702,
                -0.212543935987133,
            ]
        )
        v = numpy.array(
            [
                0.016209591718306,
                0.064838366873225,
                0.097257550309837,
                0.064838366873225,
                0.01620959171830,
            ]
        )
        s = numpy.array([numpy.exp(1j * math.pi * x / ((len(u) - 1) * 2)) for x in range(1, (len(u) - 1) * 2, 2)])
        t = math.asinh(1.0 / ((10.0 ** (0.1 * ripple) - 1.0) ** 0.5)) / (len(u) - 1)
        a = (numpy.poly((-math.sinh(t) * s.imag + 1j * math.cosh(t) * s.real) * 2.0 * math.pi)).real
        a /= a[-1]
        b = [1.0]
        a, b = ZTransform.transform(a, b, frequency, True)
        b = numpy.poly(-numpy.ones((len(u) - 1)))
        b *= (1.0 - sum(a)) / sum(b)
        assert numpy.allclose(a, u)
        assert numpy.allclose(b, v)
        frequency = 0.025
        u = numpy.array(
            [
                0.000000000000000,
                4.913032434807922,
                -10.502699472790392,
                12.647757190438988,
                -9.256183138855487,
                4.112750158020544,
                -1.0263940516247210,
                0.110901278364195,
            ]
        )
        v = (
            numpy.array(
                [
                    0.000000000160721,
                    0.002515288055351,
                    0.103543670353901,
                    0.397913857193261,
                    0.290734727994417,
                    0.040371147586715,
                    0.000522947605366,
                    0.000000000000000,
                ]
            )
            * 1.0e-3
        )
        s, a = numpy.ones(1), numpy.ones(2)
        for ii in range(2, len(u)):
            x = numpy.concatenate((s, numpy.zeros(2))) + numpy.concatenate(([0.0], ((2.0 * ii) - 1.0) * a))
            s, a = a, x
        a /= a[-1]
        b = [1.0]
        a, b = ZTransform.transform(a, b, frequency, False)
        assert numpy.allclose(a, u)
        assert numpy.allclose(b, v)
