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

from diamondback import GaussianModel


class TestGaussianModel(object):
    """Test GaussianModel."""

    def test_init(self):
        """Test init."""

        gaussian_model = GaussianModel(1.0e-1)
        assert numpy.isclose(gaussian_model.regularize, 1.0e-1)
        gaussian_model.regularize = 0.0
        assert numpy.isclose(gaussian_model.regularize, 0.0)
        u = [[1.0, 1.0], [-1.0, 1.0], [-1.0, -1.0], [1.0, -1.0]]
        x = numpy.random.randn(1000, 2) * 1.0e-1
        y = numpy.random.randint(0, len(u), x.shape[0])
        for ii in range(0, len(u)):
            jj = numpy.where(y == ii)[0]
            x[jj] += u[ii]
        gaussian_model.fit(x, y)
        v = gaussian_model.predict(x)[:, 0]
        assert sum(v == y) >= 0.95 * len(y)
