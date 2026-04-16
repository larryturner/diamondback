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

from diamondback import ComplexExponentialFilter


class TestComplexExponentialFilter(object):
    """Test ComplexExponentialFilter."""

    def test_init(self):
        """Test init."""

        phase = numpy.random.rand() * 2.0 - 1.0
        complex_exponential_filter = ComplexExponentialFilter(phase)
        assert numpy.isclose(complex_exponential_filter.phase, phase)
        phase = 1.0 / 3.0
        complex_exponential_filter.phase = phase
        assert numpy.isclose(complex_exponential_filter.phase, phase)
        z = numpy.array(
            [
                0.500000000000000 + 0.866025403784439j,
                0.500000000000000 + 0.866025403784439j,
                0.406736643075800 + 0.913545457642601j,
                0.207911690817759 + 0.978147600733806j,
                -0.104528463267653 + 0.994521895368273j,
                -0.500000000000000 + 0.866025403784439j,
                -0.866025403784438 + 0.500000000000000j,
                -0.994521895368273 - 0.104528463267653j,
                -0.669130606358858 - 0.743144825477394j,
                0.104528463267653 - 0.994521895368273j,
                0.866025403784438 - 0.500000000000000j,
                0.866025403784439 + 0.499999999999999j,
                -0.104528463267653 + 0.994521895368273j,
                -0.978147600733805 + 0.207911690817761j,
                -0.406736643075801 - 0.913545457642601j,
                0.866025403784438 - 0.500000000000001j,
                0.500000000000001 + 0.866025403784438j,
                -0.866025403784438 + 0.500000000000002j,
                -0.707106781186547 - 0.707106781186548j,
                0.258819045102520 - 0.965925826289069j,
                0.866025403784439 - 0.500000000000000j,
                1.000000000000000 - 0.000000000000001j,
                0.965925826289069 + 0.258819045102518j,
                0.965925826289069 + 0.258819045102518j,
                1.000000000000000 - 0.000000000000001j,
                0.866025403784439 - 0.500000000000000j,
                0.258819045102520 - 0.965925826289069j,
                -0.707106781186547 - 0.707106781186548j,
                -0.866025403784438 + 0.500000000000002j,
                0.500000000000001 + 0.866025403784438j,
                0.707106781186547 - 0.707106781186548j,
                -0.965925826289068 - 0.258819045102520j,
            ]
        )
        x = numpy.concatenate(
            (
                numpy.linspace(0.0, 0.5, len(z) // 2),
                numpy.linspace(0.5, -0.75, len(z) // 2),
            )
        )
        y = complex_exponential_filter.filter(x)
        assert numpy.allclose(y, z)
        assert numpy.isclose(complex_exponential_filter.phase, numpy.fmod(phase + sum(x), 2.0))
