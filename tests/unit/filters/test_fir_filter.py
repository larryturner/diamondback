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

from diamondback import ComplexExponentialFilter, FirFilter


class TestFirFilter(object):
    """Test FirFilter."""

    def test_init(self):
        """Test init."""

        b = numpy.array(
            [
                0.0000000000,
                -0.0000162201,
                -0.0003644327,
                -0.0014346038,
                -0.0033373634,
                -0.0057041661,
                -0.0076157971,
                -0.0077080371,
                -0.0044527741,
                0.0034421886,
                0.0166144204,
                0.0347262516,
                0.0563437481,
                0.0790709678,
                0.0999305645,
                0.1159157397,
                0.1245895136,
                0.1245895136,
                0.1159157397,
                0.0999305645,
                0.0790709678,
                0.0563437481,
                0.0347262516,
                0.0166144204,
                0.0034421886,
                -0.0044527741,
                -0.0077080371,
                -0.0076157971,
                -0.0057041661,
                -0.0033373634,
                -0.0014346038,
                -0.0003644327,
                -0.0000162201,
                0.0000000000,
            ]
        )
        fir_filter = FirFilter(style="Hann", frequency=0.1, order=len(b) - 1, count=1)
        assert numpy.allclose(fir_filter.b, b)
        b = numpy.array(
            [
                -0.0057980331,
                -0.0077392458,
                0.0325796910,
                0.1679693770,
                0.3129882109,
                0.3129882109,
                0.1679693770,
                0.0325796910,
                -0.0077392458,
                -0.0057980331,
            ]
        )
        fir_filter = FirFilter(style="Hamming", frequency=0.25, order=len(b) - 1, count=1)
        assert numpy.allclose(fir_filter.b, b)
        fir_filter = FirFilter(b=b, s=numpy.zeros(len(b)))
        assert numpy.allclose(fir_filter.b, b)
        fir_filter = FirFilter(style="Hann", frequency=0.2, order=16, count=1)
        assert numpy.isclose(sum(fir_filter.b), 1.0)
        z = numpy.array(
            [
                0.1000000000,
                0.1000000000,
                0.1004212703,
                0.1039277944,
                0.1130793503,
                0.1210057824,
                0.1048066472,
                0.0339499843,
                -0.1093357765,
                -0.3146837842,
                -0.5450891118,
                -0.7519440424,
                -0.8928483789,
                -0.9433506215,
                -0.8982618211,
                -0.7647982125,
                -0.5562555476,
                -0.2921269227,
                0.0005971208,
                0.2921269227,
                0.5550613059,
                0.7647982125,
                0.8996713414,
                0.9453425798,
                0.8984770998,
                0.7647982125,
                0.5562555476,
                0.2921269227,
                -0.0005971208,
                -0.2921269227,
                -0.5550613059,
                -0.7647982125,
            ]
        )
        x = ComplexExponentialFilter(0.5).filter(numpy.ones(len(z)) * 0.1).real
        n = ComplexExponentialFilter(0.0).filter(numpy.ones(len(z)) * 0.5).real * 0.1
        d = x + n
        fir_filter.reset(d[0])
        assert numpy.allclose(fir_filter.s, d[0])
        y = fir_filter.filter(d)
        assert numpy.allclose(y, z)
