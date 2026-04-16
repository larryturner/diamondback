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

from diamondback import DiversityModel


class TestDiversityModel(object):
    """Test DiversityModel."""

    def test_init(self):
        """Test init."""

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
        y = diversity_model.fit(x)
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
