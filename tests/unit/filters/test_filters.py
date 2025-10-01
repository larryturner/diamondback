"""**Description**
    Test *diamondback* *filters*.

**Example**

    ::

        pytest --capture=no --verbose

**License**
    `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
    © 2018 - 2025 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

**Author**
    Larry Turner, Schneider Electric, AI Hub, 2018-04-03.
"""

from diamondback import FirFilter, IirFilter, ComplexBandpassFilter, ComplexExponentialFilter
from diamondback import ComplexFrequencyFilter, DerivativeFilter, GoertzelFilter, IntegralFilter
from diamondback import PidFilter, PolynomialRateFilter, PolyphaseRateFilter, RankFilter
from diamondback import WindowFilter
import math
import numpy


class Test(object):
    """Test."""

    def test_ComplexBandpassFilter(self):
        """Test ComplexBandpassFilter."""

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

    def test_ComplexExponentialFilter(self):
        """Test ComplexExponentialFilter."""

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

    def test_ComplexFrequencyFilter(self):
        """Test ComplexFrequencyFilter."""

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

    def test_DerivativeFilter(self):
        """Test DerivativeFilter."""

        count = 1024
        b, derivative = numpy.array([-1.0, 8.0, 0.0, -8.0, 1.0]) * (1.0 / 12.0), 1
        derivative_filter = DerivativeFilter(derivative, len(b) - 1)
        assert numpy.allclose(derivative_filter.b, b)
        b = numpy.array([1.0, -1.0])
        derivative_filter = DerivativeFilter(derivative, len(b) - 1)
        assert numpy.allclose(derivative_filter.b, b)
        x = numpy.random.randn(count) / 2.0
        x[0] = 0.0
        d = numpy.zeros(count)
        for ii in range(1, count):
            d[ii] = d[ii - 1] + x[ii]
        derivative_filter.reset(d[0])
        assert numpy.allclose(derivative_filter.s, d[0])
        y = derivative_filter.filter(d)
        assert numpy.allclose(y, x)

    def test_FirFilter(self):
        """Test FirFilter."""

        b = numpy.array(
            [
                0.0000000000e00,
                -1.6216717596e-05,
                -3.6442085109e-04,
                -1.4345850653e-03,
                -3.3373491103e-03,
                -5.7041757801e-03,
                -7.6158521029e-03,
                -7.7081520260e-03,
                -4.4529481869e-03,
                3.4419758016e-03,
                1.6614207761e-02,
                3.4726088610e-02,
                5.6343682524e-02,
                7.9071032167e-02,
                9.9930765617e-02,
                1.1591605454e-01,
                1.2458989282e-01,
                1.2458989282e-01,
                1.1591605454e-01,
                9.9930765617e-02,
                7.9071032167e-02,
                5.6343682524e-02,
                3.4726088610e-02,
                1.6614207761e-02,
                3.4419758016e-03,
                -4.4529481869e-03,
                -7.7081520260e-03,
                -7.6158521029e-03,
                -5.7041757801e-03,
                -3.3373491103e-03,
                -1.4345850653e-03,
                -3.6442085109e-04,
                -1.6216717596e-05,
                0.0000000000e00,
            ]
        )
        fir_filter = FirFilter(style="Hann", frequency=0.1, order=len(b) - 1, count=1)
        assert numpy.allclose(fir_filter.b, b)
        b = numpy.array(
            [
                -0.0057982961,
                -0.0077523984,
                0.0325469666,
                0.1679628694,
                0.3130408585,
                0.3130408585,
                0.1679628694,
                0.0325469666,
                -0.0077523984,
                -0.0057982961,
            ]
        )
        fir_filter = FirFilter(style="Hamming", frequency=0.25, order=len(b) - 1, count=1)
        assert numpy.allclose(fir_filter.b, b)
        fir_filter = FirFilter(b=b, s=numpy.zeros(len(b)))
        assert numpy.allclose(fir_filter.b, b)
        fir_filter = FirFilter(style="Hann", frequency=0.2, order=16, count=1)
        assert numpy.isclose(sum(fir_filter.b), 1.0)
        z = numpy.array(
            [
                1.00000000e-01,
                1.00000000e-01,
                1.00421255e-01,
                1.03927757e-01,
                1.13079398e-01,
                1.21006163e-01,
                1.04807534e-01,
                3.39511979e-02,
                -1.09334744e-01,
                -3.14683417e-01,
                -5.45089567e-01,
                -7.51945156e-01,
                -8.92849866e-01,
                -9.43352225e-01,
                -8.98263340e-01,
                -7.64799495e-01,
                -5.56256475e-01,
                -2.92127412e-01,
                5.97116498e-04,
                2.92127412e-01,
                5.55062242e-01,
                7.64799495e-01,
                8.99672844e-01,
                9.45344165e-01,
                8.98478611e-01,
                7.64799495e-01,
                5.56256475e-01,
                2.92127412e-01,
                -5.97116498e-04,
                -2.92127412e-01,
                -5.55062242e-01,
                -7.64799495e-01,
            ]
        )
        x = ComplexExponentialFilter(0.5).filter(numpy.ones(len(z)) * 0.1).real
        n = ComplexExponentialFilter(0.0).filter(numpy.ones(len(z)) * 0.5).real * 0.1
        d = x + n
        fir_filter.reset(d[0])
        assert numpy.allclose(fir_filter.s, d[0])
        y = fir_filter.filter(d)
        assert numpy.allclose(y, z)

    def test_GoertzelFilter(self):
        """Test GoertzelFilter."""

        count = 1024
        frequency = 0.1
        b = WindowFilter("Hann", count - 1).b
        goertzel_filter = GoertzelFilter(b, frequency)
        for ii in range(0, 4):
            v = numpy.random.rand()
            x = ComplexExponentialFilter(numpy.random.rand()).filter(numpy.ones(count * 4) * frequency) * v
            if ii % 1:
                x = x.real
            y = goertzel_filter.filter(x)
            assert numpy.allclose(abs(y), v)

    def test_IirFilter(self):
        """Test IirFilter."""

        a = numpy.array([0.0000000000, 3.11345435, -4.016479371, 2.670363629, -0.9113738389, 0.1273250395])
        b = numpy.array([0.0005221935, 0.0026109674, 0.0052219348, 0.0052219348, 0.0026109674, 0.0005221935])
        iir_filter = IirFilter(style="Bessel", frequency=0.1, order=len(b) - 1, count=1)
        assert numpy.allclose(iir_filter.a, a)
        assert numpy.allclose(iir_filter.b, b)
        iir_filter = IirFilter(a=a, b=b, s=numpy.zeros(len(a)))
        assert numpy.allclose(iir_filter.a, a)
        assert numpy.allclose(iir_filter.b, b)
        a = numpy.array(
            [0.0000000000, 5.3932124849, -12.1474251704, 14.6237875666, -9.9230485708, 3.5980635339, -0.5446010676]
        )
        b = numpy.array(
            [
                1.7536549721e-07,
                1.0521929832e-06,
                2.6304824581e-06,
                3.5073099441e-06,
                2.6304824581e-06,
                1.0521929832e-06,
                1.7536549721e-07,
            ]
        )
        iir_filter = IirFilter(style="Butterworth", frequency=0.05, order=len(b) - 1, count=1)
        assert numpy.allclose(iir_filter.a, a)
        assert numpy.allclose(iir_filter.b, b)
        assert numpy.allclose(iir_filter.s, 0.0)
        z = numpy.array(
            [
                1.753654971914e-08,
                1.456067183425e-07,
                3.895529756880e-07,
                -7.390432379724e-07,
                -1.039304228348e-05,
                -4.907830466681e-05,
                -1.610293252688e-04,
                -4.253892439800e-04,
                -9.659936397280e-04,
                -1.957319287929e-03,
                -3.624159774970e-03,
                -6.233451546404e-03,
                -1.007803925531e-02,
                -1.545316856035e-02,
                -2.262720984575e-02,
                -3.180913888176e-02,
                -4.311629168853e-02,
                -5.654606814920e-02,
                -7.195477308227e-02,
                -8.904638597528e-02,
                -1.073735611528e-01,
                -1.263519372073e-01,
                -1.452872172607e-01,
                -1.634133228871e-01,
                -1.799391268515e-01,
                -1.941002279746e-01,
                -2.052112711932e-01,
                -2.127142284713e-01,
            ]
        )
        x = ComplexExponentialFilter(0.5).filter(numpy.ones(len(z)) * 0.1).real
        n = ComplexExponentialFilter(0.0).filter(numpy.ones(len(z)) * 0.5).real * 0.1
        d = x + n
        y = iir_filter.filter(d)
        assert numpy.allclose(y, z)
        iir_filter.reset(d[0])
        s = numpy.ones(len(iir_filter.a)) * 8909.962478155508
        s[0] = d[0]
        assert numpy.allclose(s, iir_filter.s)
        z = numpy.array(
            [
                0.100000000000,
                0.099999928273,
                0.099999044643,
                0.099993654638,
                0.099971704264,
                0.099903792042,
                0.099731727295,
                0.099356711892,
                0.098629435885,
                0.097344537594,
                0.095241822188,
                0.092015733855,
                0.087333189226,
                0.080858870433,
                0.072286360297,
                0.06137248622,
                0.047971259902,
                0.032063657924,
                0.01377999136,
                -0.006587971867,
                -0.028587460781,
                -0.051618820228,
                -0.074962750943,
                -0.097818954524,
                -0.119353657877,
                -0.138752440686,
                -0.155273822427,
                -0.168298973585,
            ]
        )
        y = iir_filter.filter(d)
        assert numpy.allclose(y, z)
        a = numpy.array([0.0000000000, 3.8765072084, -5.6415809915, 3.653029515, -0.8879718207])
        b = numpy.array([1.0055554834e-06, 4.0222219335e-06, 6.0333329003e-06, 4.0222219335e-06, 1.0055554834e-06])
        iir_filter = IirFilter(style="Chebyshev", frequency=0.025, order=len(b) - 1, count=2)
        assert numpy.allclose(iir_filter.a, a)
        assert numpy.allclose(iir_filter.b, b)

    def test_IntegralFilter(self):
        """Test IntegralFilter."""

        count = 128
        a = numpy.array([0.0, 1.0, 0.0, 0.0, 0.0])
        b = numpy.array([7.0, 32.0, 12.0, 32.0, 7.0]) * (1.0 / 90.0)
        integral_filter = IntegralFilter(len([x for x in b if (not numpy.isclose(x, 0.0))]) - 1)
        assert numpy.allclose(integral_filter.a, a)
        assert numpy.allclose(integral_filter.b, b)
        a = numpy.array([0.0, 1.0])
        b = numpy.array([1.0, 1.0]) * (1.0 / 2.0)
        integral_filter = IntegralFilter(len([x for x in b if (not numpy.isclose(x, 0.0))]) - 1)
        assert numpy.allclose(integral_filter.a, a)
        assert numpy.allclose(integral_filter.b, b)
        a = numpy.array([0.0, 1.0])
        b = numpy.array([1.0, 0.0])
        integral_filter = IntegralFilter(len([x for x in b if (not numpy.isclose(x, 0.0))]) - 1)
        assert numpy.allclose(integral_filter.a, a)
        assert numpy.allclose(integral_filter.b, b)
        x = numpy.random.randn(count) / 2.0
        x[0] = 0.0
        d = numpy.zeros(count)
        for ii in range(1, count):
            d[ii] = d[ii - 1] + x[ii]
        integral_filter.reset(x[0])
        assert numpy.allclose(integral_filter.s, x[0])
        y = integral_filter.filter(x)
        assert numpy.allclose(y, d)

    def test_PidFilter(self):
        """Test PidFilter."""

        count = 1024
        limit = 1.5
        b = numpy.random.randn(3)
        pid_filter = PidFilter(b)
        assert numpy.allclose(pid_filter.b, b)
        pid_filter.limit = limit
        assert numpy.isclose(pid_filter.limit, limit)
        pid_filter.limit = numpy.inf
        assert numpy.isclose(pid_filter.limit, numpy.inf)
        x = numpy.random.randn(count)
        y = pid_filter.filter(x)
        assert len(y) == count

    def test_PolynomialRateFilter(self):
        """Test PolynomialRateFilter."""

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

    def test_PolyphaseRateFilter(self):
        """Test PolyphaseRateFilter."""

        count = 128
        frequency, rate = math.pi * 0.1, math.pi
        polyphase_rate_filter = PolyphaseRateFilter(0.1)
        assert numpy.isclose(polyphase_rate_filter.rate, 0.1)
        polyphase_rate_filter.rate = rate
        assert numpy.isclose(polyphase_rate_filter.rate, rate)
        x = ComplexExponentialFilter(0.5).filter(numpy.ones(count) * frequency).real
        polyphase_rate_filter.reset(x[0])
        assert numpy.allclose(polyphase_rate_filter.s, x[0])
        y = polyphase_rate_filter.filter(x)
        assert numpy.isclose(len(y), numpy.floor(count * rate)) or numpy.isclose(len(y), numpy.ceil(count * rate))
        rate, count = 1.0 / rate, len(y)
        polyphase_rate_filter.rate = rate
        polyphase_rate_filter.reset(y[0])
        z = polyphase_rate_filter.filter(y)
        assert numpy.isclose(len(z), numpy.floor(count * rate)) or numpy.isclose(len(z), numpy.ceil(count * rate))
        rate, count = 0.25, 64
        x = numpy.concatenate(
            (
                numpy.linspace(-1.0, 1.0, count // 2),
                numpy.linspace(1.0, -1.0, count // 2),
            )
        )
        polyphase_rate_filter.rate = rate
        polyphase_rate_filter.reset(0.0)
        y = polyphase_rate_filter.filter(x)
        z = numpy.array(
            [
                0.00000000,
                0.02061912,
                -1.09636725,
                -0.71004968,
                -0.45148771,
                -0.19342319,
                0.06464132,
                0.32270584,
                0.58077036,
                0.83952135,
                0.97098504,
                0.70966357,
                0.45148771,
                0.19342319,
                -0.06464132,
                -0.32270584,
            ]
        )
        assert numpy.allclose(y, z)

    def test_RankFilter(self):
        """Test RankFilter."""

        index, order = 4, 4
        rank_filter = RankFilter(index, order)
        assert rank_filter.index == index
        assert len(rank_filter.s) == order + 1
        x = numpy.concatenate(
            (
                numpy.ones(1),
                numpy.zeros(15),
                numpy.ones(4),
                numpy.zeros(2),
                numpy.ones(5),
                numpy.zeros(6),
            )
        )
        rank_filter.reset(x[0])
        assert numpy.allclose(rank_filter.s, x[0])
        y = rank_filter.filter(x)
        z = numpy.concatenate((numpy.ones(5), numpy.zeros(11), numpy.ones(15), numpy.zeros(2)))
        assert numpy.allclose(y, z)

    def test_WindowFilter(self):
        """Test WindowFilter."""

        b = numpy.array(
            [
                0.00000000,
                0.04322727,
                0.16543470,
                0.34549150,
                0.55226423,
                0.75000000,
                0.90450850,
                0.98907380,
                0.98907380,
                0.90450850,
                0.75000000,
                0.55226423,
                0.34549150,
                0.16543470,
                0.04322727,
                0.00000000,
            ]
        )
        window_filter = WindowFilter("Hann", len(b) - 1, False)
        assert numpy.allclose(window_filter.b, b)
        window_filter = WindowFilter("Hann", len(b) - 1, True)
        assert numpy.allclose(window_filter.b, b * len(b) / sum(abs(b)))
