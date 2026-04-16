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

from diamondback import GaussianMixtureModel


class TestGaussianMixtureModel(object):
    """Test GaussianMixtureModel."""

    def test_init(self):
        """Test init."""

        gaussian_mixture_model = GaussianMixtureModel(2, 20, 0.0)
        assert gaussian_mixture_model.order == 2
        assert gaussian_mixture_model.index == 20
        gaussian_mixture_model.index = 100
        assert gaussian_mixture_model.index == 100
        assert numpy.isclose(gaussian_mixture_model.regularize, 0.0)
        gaussian_mixture_model.regularize = 1.0e-1
        assert numpy.isclose(gaussian_mixture_model.regularize, 1.0e-1)
        u = [
            [0.5, 0.5],
            [1.0, 1.0],
            [-0.5, 0.5],
            [-1.0, 1.0],
            [-0.5, -0.5],
            [-1.0, -1.0],
            [0.5, -0.5],
            [1.0, -1.0],
        ]
        x = numpy.random.randn(1000, 2) * 1.0e-1
        y = numpy.random.randint(0, len(u), x.shape[0])
        for ii in range(0, len(u)):
            jj = numpy.where(y == ii)[0]
            x[jj] += u[ii]
        y >>= 1
        gaussian_mixture_model.fit(x, y)
        v = gaussian_mixture_model.predict(x)[:, 0]
        assert sum(v == y) >= 0.95 * len(y)
