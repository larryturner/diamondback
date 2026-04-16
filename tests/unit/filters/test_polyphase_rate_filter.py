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

import math

import numpy

from diamondback import ComplexExponentialFilter, PolyphaseRateFilter


class TestPolyphaseRateFilter(object):
    """Test PolyphaseRateFilter."""

    def test_init(self):
        """Test init."""

        count = 128
        frequency, rate = math.pi * 0.1, math.pi
        polyphase_rate_filter = PolyphaseRateFilter(0.1)
        assert numpy.isclose(polyphase_rate_filter.rate, 0.1)
        polyphase_rate_filter.rate = rate
        assert numpy.isclose(polyphase_rate_filter.rate, rate)
        x = ComplexExponentialFilter(0.5).filter(numpy.ones(count) * frequency).real
        polyphase_rate_filter.reset(x[0])
        assert numpy.allclose(polyphase_rate_filter.s, x[0])
        y = polyphase_rate_filter.filter(x)
        assert numpy.isclose(len(y), numpy.floor(count * rate)) or numpy.isclose(len(y), numpy.ceil(count * rate))
        rate, count = 1.0 / rate, len(y)
        polyphase_rate_filter.rate = rate
        polyphase_rate_filter.reset(y[0])
        z = polyphase_rate_filter.filter(y)
        assert numpy.isclose(len(z), numpy.floor(count * rate)) or numpy.isclose(len(z), numpy.ceil(count * rate))
        rate, count = 0.25, 64
        x = numpy.concatenate(
            (
                numpy.linspace(-1.0, 1.0, count // 2),
                numpy.linspace(1.0, -1.0, count // 2),
            )
        )
        polyphase_rate_filter.rate = rate
        polyphase_rate_filter.reset(0.0)
        y = polyphase_rate_filter.filter(x)
        z = numpy.array(
            [
                0.00000000,
                0.02061912,
                -1.09636725,
                -0.71004968,
                -0.45148771,
                -0.19342319,
                0.06464132,
                0.32270584,
                0.58077036,
                0.83952135,
                0.97098504,
                0.70966357,
                0.45148771,
                0.19342319,
                -0.06464132,
                -0.32270584,
            ]
        )
        assert numpy.allclose(y, z)
