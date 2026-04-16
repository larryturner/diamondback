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

import math

import numpy

from diamondback import ComplexExponentialFilter, PolynomialRateFilter


class TestPolynomialRateFilter(object):
    """Test PolynomialRateFilter."""

    def test_init(self):
        """Test init."""

        count = 32
        frequency, order = math.pi * 0.1, 3
        rate = math.pi
        r = numpy.random.rand() * 10.0 + 1.0
        polynomial_rate_filter = PolynomialRateFilter(r, order)
        assert numpy.isclose(polynomial_rate_filter.rate, r)
        polynomial_rate_filter.rate = rate
        assert numpy.isclose(polynomial_rate_filter.rate, rate)
        x = ComplexExponentialFilter(0.5).filter(numpy.ones(count) * frequency).real
        y = polynomial_rate_filter.filter(x)
        z = numpy.array(
            [
                -1.50938920e-15,
                -3.01286605e-01,
                -5.78421038e-01,
                -8.07251126e-01,
                -9.35300681e-01,
                -9.80311079e-01,
                -9.44846453e-01,
                -7.99720095e-01,
                -5.75258456e-01,
                -3.03927650e-01,
                -2.88149434e-03,
                3.02702761e-01,
                5.83528284e-01,
                8.00381555e-01,
                9.31518449e-01,
                9.86496972e-01,
                9.45905739e-01,
                7.93857933e-01,
                5.76364443e-01,
                3.09155188e-01,
                1.97908969e-03,
                -3.06078665e-01,
                -5.87611199e-01,
                -7.93455291e-01,
                -9.33972480e-01,
                -9.97190305e-01,
                -9.36926168e-01,
                -7.92272692e-01,
                -5.82874118e-01,
                -3.07568750e-01,
                7.84550105e-04,
                3.08790848e-01,
                5.78688584e-01,
                7.92470898e-01,
                9.41440696e-01,
                9.91029455e-01,
                9.31913194e-01,
                7.96464675e-01,
                5.85774047e-01,
                3.04173769e-01,
                -2.84387507e-03,
                -3.06800272e-01,
                -5.75134650e-01,
                -7.96631541e-01,
                -9.50649339e-01,
                -9.82462303e-01,
                -9.32768893e-01,
                -8.06310373e-01,
                -5.80702911e-01,
                -3.01540819e-01,
                1.87274326e-03,
                3.01915167e-01,
                5.76559550e-01,
                8.03758347e-01,
                9.39084678e-01,
                9.79501593e-01,
                9.39826199e-01,
                8.03169181e-01,
                5.76308538e-01,
                3.02115621e-01,
                2.09267642e-03,
                -3.01656744e-01,
                -5.81104941e-01,
                -8.05385284e-01,
                -9.32476390e-01,
                -9.82943717e-01,
                -9.50588784e-01,
                -7.96171920e-01,
                -5.75215932e-01,
                -3.07380275e-01,
                -2.76802714e-03,
                3.04442192e-01,
                5.86112809e-01,
                7.95928727e-01,
                9.32106032e-01,
                9.91862011e-01,
                9.40740088e-01,
                7.92343961e-01,
                5.79191217e-01,
                3.08662743e-01,
                5.63419210e-04,
                -3.07784965e-01,
                -5.82182945e-01,
                -7.92199630e-01,
                -9.37509152e-01,
                -9.96269822e-01,
                -9.33580539e-01,
                -7.93778141e-01,
                -5.87588041e-01,
                -3.05808939e-01,
                2.14525625e-03,
                3.09141999e-01,
                5.76092393e-01,
                7.94185235e-01,
                9.46680110e-01,
                9.61139947e-01,
                8.89551638e-01,
                7.78862770e-01,
                6.84415649e-01,
                6.07716745e-01,
                5.31017840e-01,
            ]
        )
        assert numpy.allclose(y, z)
