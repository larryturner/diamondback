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

from diamondback import DerivativeFilter


class TestDerivativeFilter(object):
    """Test DerivativeFilter."""

    def test_init(self):
        """Test init."""

        count = 1024
        b, derivative = numpy.array([-1.0, 8.0, 0.0, -8.0, 1.0]) * (1.0 / 12.0), 1
        derivative_filter = DerivativeFilter(derivative, len(b) - 1)
        assert numpy.allclose(derivative_filter.b, b)
        b = numpy.array([1.0, -1.0])
        derivative_filter = DerivativeFilter(derivative, len(b) - 1)
        assert numpy.allclose(derivative_filter.b, b)
        x = numpy.random.randn(count) / 2.0
        x[0] = 0.0
        d = numpy.zeros(count)
        for ii in range(1, count):
            d[ii] = d[ii - 1] + x[ii]
        derivative_filter.reset(d[0])
        assert numpy.allclose(derivative_filter.s, d[0])
        y = derivative_filter.filter(d)
        assert numpy.allclose(y, x)
