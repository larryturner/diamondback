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

import numpy

from diamondback import ComplexExponentialFilter, PsdTransform, WindowFilter


class TestPsdTransform(object):
    """Test PsdTransform."""

    def test_init(self):
        """Test init."""

        count = 128
        frequency, index = (0.12, 0.23), 64
        b = WindowFilter("Hann", count - 1).b
        for ii in range(0, 2):
            x = numpy.random.rand() * ComplexExponentialFilter(numpy.random.rand()).filter(
                numpy.linspace(frequency[0], frequency[1], count * 8)
            )
            if ii > 0:
                x = x.real
            y, f = PsdTransform.transform(x, b, index, False)
            assert (len(y) == (count // 2)) and (len(f) == (count // 2))
            assert not isinstance(y[0], complex)
            assert numpy.isclose(f[0], 0.0) and numpy.isclose(f[-1], 1.0 - 2.0 / count)
