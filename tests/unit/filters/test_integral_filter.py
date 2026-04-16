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

from diamondback import IntegralFilter


class TestIntegralFilter(object):
    """Test IntegralFilter."""

    def test_init(self):
        """Test init."""

        count = 128
        a = numpy.array([0.0, 1.0, 0.0, 0.0, 0.0])
        b = numpy.array([7.0, 32.0, 12.0, 32.0, 7.0]) * (1.0 / 90.0)
        integral_filter = IntegralFilter(len([x for x in b if (not numpy.isclose(x, 0.0))]) - 1)
        assert numpy.allclose(integral_filter.a, a)
        assert numpy.allclose(integral_filter.b, b)
        a = numpy.array([0.0, 1.0])
        b = numpy.array([1.0, 1.0]) * (1.0 / 2.0)
        integral_filter = IntegralFilter(len([x for x in b if (not numpy.isclose(x, 0.0))]) - 1)
        assert numpy.allclose(integral_filter.a, a)
        assert numpy.allclose(integral_filter.b, b)
        a = numpy.array([0.0, 1.0])
        b = numpy.array([1.0, 0.0])
        integral_filter = IntegralFilter(len([x for x in b if (not numpy.isclose(x, 0.0))]) - 1)
        assert numpy.allclose(integral_filter.a, a)
        assert numpy.allclose(integral_filter.b, b)
        x = numpy.random.randn(count) / 2.0
        x[0] = 0.0
        d = numpy.zeros(count)
        for ii in range(1, count):
            d[ii] = d[ii - 1] + x[ii]
        integral_filter.reset(x[0])
        assert numpy.allclose(integral_filter.s, x[0])
        y = integral_filter.filter(x)
        assert numpy.allclose(y, d)
