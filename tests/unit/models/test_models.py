"""**Description**
    Test *diamondback* *models*.

**Example**

    ::

        pytest --capture=no --verbose

**License**
    `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_
    © 2018 - 2025 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

**Author**
    Larry Turner, Schneider Electric, AI Hub, 2018-04-03.
"""

from diamondback import DiversityModel, GaussianModel, GaussianMixtureModel
import numpy


class Test(object):
    """Test."""

    def test_DiversityModel(self):
        """Test DiversityModel."""

        ii = [11, 1, 2, 3, 10]
        diversity_model = DiversityModel("Euclidean", len(ii) - 1)
        assert diversity_model.s.shape == (len(ii), 0)
        x = numpy.array(
            [
                [0.929263623187228, 0.349983765984809],
                [0.232958886794845, 0.323811130703304],
                [0.688771948873912, 0.618743394357275],
                [0.460750416153906, 1.049010446078109],
                [0.730718636607270, 0.840632699200231],
                [1.099011845647992, 0.649475382456737],
                [0.975382047292540, 1.190092730642132],
                [0.634991301520811, 1.076912549816130],
                [0.366763380472155, 0.635768300484789],
                [0.858070280281700, 1.433712684647466],
                [1.297647047865546, 0.857178935746457],
                [0.968823660872193, 1.269390641058206],
            ]
        )
        y = diversity_model.learn(x)
        v = numpy.array(
            [
                0.000000,
                0.000000,
                0.000000,
                0.000000,
                0.000000,
                0.344252,
                0.411389,
                0.411389,
                0.411389,
                0.411389,
                0.463343,
                0.486953,
            ]
        )
        s = x[ii, :]
        assert numpy.allclose(y, v)
        assert numpy.allclose(s, diversity_model.s)

    def test_GaussianModel(self):
        """Test GaussianModel."""

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
        gaussian_model.learn(x, y)
        v = gaussian_model.predict(x)[:, 0]
        assert sum(v == y) >= 0.95 * len(y)

    def test_GaussianMixtureModel(self):
        """Test GaussianMixtureModel."""

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
        gaussian_mixture_model.learn(x, y)
        v = gaussian_mixture_model.predict(x)[:, 0]
        assert sum(v == y) >= 0.95 * len(y)
