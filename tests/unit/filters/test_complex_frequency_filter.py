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

from diamondback import ComplexExponentialFilter, ComplexFrequencyFilter


class TestComplexFrequencyFilter(object):
    """Test ComplexFrequencyFilter."""

    def test_init(self):
        """Test init."""

        count = 128
        frequency, rate = numpy.random.rand() * 2.0 - 1.0, numpy.random.rand()
        complex_frequency_filter = ComplexFrequencyFilter(frequency, rate)
        assert numpy.isclose(complex_frequency_filter.frequency, frequency)
        assert numpy.isclose(complex_frequency_filter.rate, rate)
        frequency, rate = 0.0, 2.0e-1
        complex_frequency_filter.frequency, complex_frequency_filter.rate = frequency, rate
        assert numpy.isclose(complex_frequency_filter.frequency, frequency)
        assert numpy.isclose(complex_frequency_filter.rate, rate)
        x = numpy.concatenate(
            (
                numpy.linspace(0.0, 0.05, int(count / 4)),
                numpy.linspace(0.05, -0.05, int(count / 2)),
                numpy.ones(int(count / 4)) * -0.05,
            )
        )
        d = ComplexExponentialFilter(0.0).filter(x)
        complex_frequency_filter.reset(d[0])
        y, e, b = complex_frequency_filter.filter(d)
        assert (len(y) == count) and (len(e) == count) and (len(b) == count)
        assert abs(max(y[int(numpy.floor(0.25 * len(y))) :]) - max(x[int(numpy.floor(0.25 * len(x))) :])) < 5.0e-3
        assert abs(min(y[int(numpy.floor(0.25 * len(y))) :]) - min(x[int(numpy.floor(0.25 * len(x))) :])) < 5.0e-3
        assert abs(y[-1] - x[-1]) < 5.0e-3
