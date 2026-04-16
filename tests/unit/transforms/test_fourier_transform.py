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

from diamondback import ComplexExponentialFilter, FourierTransform, WindowFilter


class TestFourierTransform(object):
    """Test FourierTransform."""

    def test_init(self):
        """Test init."""

        count = 128
        frequency = (0.12, 0.23)
        b = numpy.ones(count)
        for ii in range(0, 4):
            x = numpy.random.rand() * ComplexExponentialFilter(numpy.random.rand()).filter(
                numpy.linspace(frequency[0], frequency[1], count)
            )
            if ii % 2:
                x = x.real
            if ii >= 2:
                b = WindowFilter("Hann", count - 1).b
            y, f = FourierTransform.transform(x, b)
            assert (len(y) == count) and (len(f) == count)
            assert isinstance(y[0], complex)
            assert numpy.isclose(f[0], -1.0) and numpy.isclose(f[-1], 1.0 - 2.0 / count)
            h = numpy.argmax(abs(y[count // 2 :]))
            assert (h >= numpy.argmin(abs(f[count // 2 :] - frequency[0]))) and (
                h <= numpy.argmin(abs(f[count // 2 :] - frequency[1]))
            )
            z = FourierTransform.transform(y, b, True)[0]
            if ii % 2:
                z = z.real
            assert numpy.allclose(z[1:-1], x[1:-1])
