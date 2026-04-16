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

from diamondback import ComplexExponentialFilter, GoertzelFilter, WindowFilter


class TestGoertzelFilter(object):
    """Test GoertzelFilter."""

    def test_init(self):
        """Test init."""

        count = 1024
        frequency = 0.1
        b = WindowFilter("Hann", count - 1).b
        goertzel_filter = GoertzelFilter(b, frequency)
        for ii in range(0, 4):
            v = numpy.random.rand()
            x = ComplexExponentialFilter(numpy.random.rand()).filter(numpy.ones(count * 4) * frequency) * v
            if ii % 1:
                x = x.real
            y = goertzel_filter.filter(x)
            assert numpy.allclose(abs(y), v)
