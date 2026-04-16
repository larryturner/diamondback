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

from diamondback import ComplexBandpassFilter, ComplexExponentialFilter


class TestComplexBandpassFilter(object):
    """Test ComplexBandpassFilter."""

    def test_init(self):
        """Test init."""

        count = 128
        frequency, rate = numpy.random.rand() * 2.0 - 1.0, numpy.random.rand()
        complex_bandpass_filter = ComplexBandpassFilter(frequency, rate)
        assert numpy.isclose(complex_bandpass_filter.frequency, frequency)
        assert numpy.isclose(complex_bandpass_filter.rate, rate)
        frequency, rate = 0.1, 5.0e-2
        complex_bandpass_filter.frequency, complex_bandpass_filter.rate = frequency, rate
        assert numpy.isclose(complex_bandpass_filter.frequency, frequency)
        assert numpy.isclose(complex_bandpass_filter.rate, rate)
        x = ComplexExponentialFilter(0.5).filter(numpy.linspace(-1.0e-4, 1.0e-4, count) + frequency)
        n = ComplexExponentialFilter(0.0).filter(numpy.linspace(-1.0e-4, 1.0e-4, count) + frequency * 3.5) * 1.0e-3
        d = x + n
        complex_bandpass_filter.reset(d[0])
        assert numpy.allclose(complex_bandpass_filter.s, d[0])
        y, e, b = complex_bandpass_filter.filter(d)
        assert (len(y) == count) and (len(e) == count) and (len(b) == count)
        assert numpy.allclose(y + e, d)
        assert numpy.average(abs(e[len(e) - 31 :])) < 5.0e-3
