"""**Description**
    A Finite Impulse Response (FIR) filter realizes a discrete difference
    equation as a function of a forward coefficient array and a state array
    of a specified order, consuming an incident signal and producing a
    reference signal.

    .. math::

        s_{i,n} = s_{i-1,n-1}\\qquad\\quad s_{0,n} = x_{n}

    .. math::

        y_{n} = \\sum_{i = 0}^{N} b_{i,n} x_{n-i} = \\sum_{i = 0}^{N} b_{i,n} s_{i,n}

    A reset may minimize edge effects at a discontinuity by assuming
    persistent operation at a specified incident signal condition.

    .. math::

        s_{i,n} = x_{n}

    A frequency response is expressed as a function of a forward
    coefficient array.

    .. math::

        H_{z,n} = \\sum_{i = 0}^{N} b_{i,n} z^{-i}

    A forward coefficient array and state array of a specified order are
    defined to realize specified constraints.  A style, frequency,
    order, count, complement, and gain are electively specified.
    Alternatively, a forward coefficient array and state array may be explicitly
    defined to ignore constraints.

    Frequency corresponds to a -3 dB frequency response normalized relative
    to Nyquist.

    Style is in ("Blackman", "Hamming", "Hann", "Kaiser").

    * | "Blackman" filters demonstrate low resolution and spectral leakage
      | with improved rate of attenuation.

    * | "Hamming" filters demonstrate minimal nearest side lobe magnitude
      | response.

    * | "Hann" filters demonstrate high resolution and spectral leakage.

    * | "Kaiser" filters demonstrate flexible resolution and spectral
      | leakage dependent upon a beta value of a Bessel function of the
      | first kind, with beta equal to 7.0.

    Order must even to ensure a Type I form linear phase solution.

    Count is a quantity of filters of a specified order concatenated to
    form an aggregate frequency response in cascade form.

    Complement effectively constructs a mirror image of a specified
    frequency response.

**Example**

    .. code-block:: python

        from diamondback import FirFilter
        import numpy

        # Constraints.

        fir_filter = FirFilter(style = "Kaiser", frequency = 0.1, order = 32, count = 1)

        # Coefficients.

        fir_filter = FirFilter(b = fir_filter.b)

        # Frequency response, group delay, and roots.

        y, f = fir_filter.response(length = 8192, count = 1)
        y, f = fir_filter.delay(length = 8192, count = 1)
        p, z = fir_filter.roots(count = 1)

        # Filter.

        x = numpy.random.rand(128) * 2.0 - 1.0
        fir_filter.reset(x[0])
        y = fir_filter.filter(x)

**License**
    `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
    © 2018 - 2025 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

**Author**
    Larry Turner, Schneider Electric, AI Hub, 2018-01-23.
"""

import math
import numpy
import scipy.signal
import warnings


class FirFilter(object):
    """Finite Impulse Response (FIR) filter."""

    STYLE = ("Blackman", "Hamming", "Hann", "Kaiser")

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, b: list | numpy.ndarray):
        self._b = b

    @property
    def s(self):
        return self._s

    @s.setter
    def s(self, s: list | numpy.ndarray):
        self._s = s

    def __init__(
        self,
        style: str = "",
        frequency: float = 0.0,
        order: int = 1,
        count: int = 1,
        complement: bool = False,
        gain: float = 1.0,
        b: list | numpy.ndarray = [],
        s: list | numpy.ndarray = [],
    ) -> None:
        """Initialize.

        Specify constraints including style, frequency, and order.
        Alternatively, a forward coefficient array may be explicitly defined
        to ignore constraints.

        Labels should be used to avoid ambiguity between constraints and
        coefficients.

        Arguments:
            style: str - in ("Blackman", "Hamming", "Hann", "Kaiser").
            frequency: float - frequency normalized to Nyquist in (0.0, 1.0).
            order: int - order per instance.
            count: int - instances per cascade.
            complement: bool - complement response.
            gain: float - gain.
            b: list | numpy.ndarray - forward coefficient.
            s: list | numpy.ndarray - state.
        """

        if not len(b):
            style = style.title()
            if style not in FirFilter.STYLE:
                raise ValueError(f"style = {style} Expected Style in {FirFilter.STYLE}")
            if (frequency <= 0.0) or (frequency >= 1.0):
                raise ValueError(f"Frequency = {frequency} Expected Frequency in (0.0, 1.0)")
            if order <= 0:
                raise ValueError(f"Order = {order} Expected Order in (0, inf)")
            if count <= 0:
                raise ValueError(f"Count = {count} Expected Count in (0, inf)")
            if complement:
                frequency = 1.0 - frequency
            if style == "Kaiser":
                window = (style.lower(), 7.0)
            else:
                window = style.lower()  # type: ignore
            beta, eps, error = 10.0, float(numpy.finfo(float).eps), numpy.inf
            index, rate, scale = 500 * (1 + (count > 2)), 2.5e-2, 1.0
            for _ in range(0, index):
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    v = scipy.signal.firwin(
                        numtaps=order + 1,
                        cutoff=min(scale * frequency, 1.0 - eps),
                        width=None,
                        window=window,
                        pass_zero=True,
                        scale=True,
                        fs=2.0,
                    )
                    if numpy.isnan(v).any():
                        raise ValueError(f"V = {v}")
                    x = numpy.exp(1j * math.pi * frequency)
                    e = (2.0 ** (-0.5)) - (abs(numpy.polyval(v, x)) ** count)
                    if abs(e) < error:
                        b, error = v, abs(e)
                        if error < (10.0 * eps):
                            break
                    scale = numpy.maximum(scale + rate * math.tanh(beta * e), eps)
            if complement:
                b *= numpy.array([((-1.0) ** x) for x in range(0, len(b))])
                b /= sum(b * numpy.array([((-1.0) ** x) for x in range(0, len(b))]))
            b *= gain  # type: ignore
        if not isinstance(b, numpy.ndarray):
            b = numpy.array(list(b))
        if not len(b):
            raise ValueError(f"B = {b}")
        if not isinstance(s, numpy.ndarray):
            s = numpy.array(list(s))
        if len(b) < len(s):
            b = numpy.concatenate((b, numpy.zeros(len(s) - len(b))))
        if len(s) < len(b):
            s = numpy.concatenate((s, numpy.zeros(len(b) - len(s))))
        super().__init__()
        self._b, self._s = numpy.array(b), numpy.array(s, type(b[0]))

    def delay(self, length: int = 8192, count: int = 1) -> tuple[numpy.ndarray, numpy.ndarray]:
        """Estimates group delay and produces a reference signal.

        Arguments:
            length: int.
            count: int.

        Returns:
            y: numpy.ndarray - reference signal.
            f: numpy.ndarray - frequency normalized to Nyquist in [-1.0, 1.0).
        """

        if length <= 0:
            raise ValueError(f"Length = {length} Expected Length in (0, inf)")
        if count <= 0:
            raise ValueError(f"Count = {count} Expected Count in (0, inf)")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            y, f = (
                scipy.signal.group_delay((self.b, [1.0]), length, True)[1],
                numpy.linspace(-1.0, 1.0 - 2.0 / length, length),
            )
            y = numpy.concatenate((y[len(y) // 2 :], y[: len(y) // 2])) * count
        if length > 2:
            y[0] = y[1] * 2.0 - y[2]
        return y, f

    def filter(self, x: list | numpy.ndarray) -> numpy.ndarray:
        """Filters an incident signal and produces a reference signal.

        Arguments:
            x: list | numpy.ndarray - incident signal.

        Returns:
            y: numpy.ndarray - reference signal.
        """

        if not isinstance(x, numpy.ndarray):
            x = numpy.array(list(x))
        if not len(x):
            raise ValueError(f"X = {x}")
        y = numpy.zeros(len(x), type(self.b[0]))
        for ii in range(0, len(x)):
            if len(self.s) > 1:
                self.s[1:] = self.s[:-1]
            self.s[0] = x[ii]
            y[ii] = self.b.dot(self.s)
        return y

    def reset(self, x: complex | float) -> None:
        """Modifies a state to minimize edge effects by assuming persistent
        operation at a specified incident signal condition.

        Arguments:
            x: complex | float - incident signal.
        """

        if not numpy.isscalar(x):
            raise ValueError(f"X = {x}")
        self.s[:] = x

    def response(self, length=8192, count=1) -> tuple[numpy.ndarray, numpy.ndarray]:
        """Estimates frequency response and produces a reference signal.

        Arguments:
            length: int.
            count: int.

        Returns:
            y: numpy.ndarray - reference signal.
            f: numpy.ndarray - frequency normalized to Nyquist in [-1.0, 1.0).
        """

        if length <= 0:
            raise ValueError(f"Length = {length} Expected Length in (0, inf)")
        if count <= 0:
            raise ValueError(f"Count = {count} Expected Count in (0, inf)")
        y, f = (
            scipy.signal.freqz(self.b, [1.0, 0.0], length, True)[1],
            numpy.linspace(-1.0, 1.0 - 2.0 / length, length),
        )
        y = numpy.concatenate((y[len(y) // 2 :], y[: len(y) // 2])) ** count
        return y, f

    def roots(self, count=1) -> tuple[numpy.ndarray, numpy.ndarray]:
        """Estimates roots of a frequency response in poles and zeros.

        Arguments:
            count: int.
        Returns:
            p: numpy.ndarray - poles.
            z: numpy.ndarray - zeros.
        """

        z = numpy.tile(numpy.roots(self.b), count)
        return numpy.zeros(count * (len(self.b) - 1)), z[numpy.argsort(abs(z))]
