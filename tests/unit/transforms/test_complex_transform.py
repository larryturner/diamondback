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

from diamondback import ComplexExponentialFilter, ComplexTransform


class TestComplexTransform(object):
    """Test ComplexTransform."""

    def test_init(self):
        """Test init."""

        count = 32
        frequency = 0.1
        x = ComplexExponentialFilter(0.5).filter(numpy.linspace(-1.0e-4, 1.0e-4, count) + frequency)
        for ii in range(0, 2):
            y = ComplexTransform.transform(x, not ii)
            assert y.shape == (3, count)
            assert not isinstance(y[0], complex)
            z = ComplexTransform.transform(y, not ii)
            assert z.shape == (count,)
            assert isinstance(z[0], complex)
            assert numpy.allclose(z, x)
