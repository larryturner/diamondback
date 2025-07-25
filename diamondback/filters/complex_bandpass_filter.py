"""**Description**
    A complex bandpass filter produces a complex exponential incident
    signal at a specified normalized frequency and adapts a forward complex
    coefficient to produce a reference signal, which estimates a component
    of interest in a primary signal.  A normalized frequency and rate of
    adaptation are specified.

    .. math::

        x_{n} = e^{\\ j\\ \\pi\\ \\phi_{n}}

    .. math::

        \\phi_{n+1} = \\phi_{n} + f_{n}

    .. math::

        y_{n} = b_{n} x_{n}

    .. math::

        e_{n} = d_{n} - y_{n}

    .. math::

        b_{n+1} = b_{n} + \\mu e_{n} x_{n}^{*}

**Example**

    .. code-block:: python

        from diamondback import ComplexBandpassFilter, ComplexExponentialFilter
        import numpy

        frequency = 0.1
        x = numpy.linspace(-1.0e-4, 1.0e-4, 128) + frequency
        d = ComplexExponentialFilter(phase = numpy.random.rand(1)[0] * 2.0 - 1.0).filter(x)
        complex_bandpass_filter = ComplexBandpassFilter(frequency = frequency, rate = 5.0e-2)
        complex_bandpass_filter.reset(d[0])
        y, e, b = complex_bandpass_filter.filter(d)

**License**
    `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
    © 2018 - 2025 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

**Author**
    Larry Turner, Schneider Electric, AI Hub, 2018-01-31.
"""

from diamondback.filters.complex_exponential_filter import ComplexExponentialFilter
from diamondback.filters.fir_filter import FirFilter
import numpy
import scipy


class ComplexBandpassFilter(FirFilter):
    """Complex bandpass filter."""

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, frequency: float):
        if (frequency < -1.0) or (frequency > 1.0):
            raise ValueError(f"Frequency = {frequency} Expected Frequency in [-1.0, 1.0]")
        self._frequency = frequency

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, rate: float):
        if (rate < 0.0) or (rate > 1.0):
            raise ValueError(f"Rate = {rate} Expected Rate in [0.0, 1.0]")
        self._rate = rate

    def __init__(self, frequency: float, rate: float) -> None:
        """Initialize.

        Arguments:
            frequency: float - frequency normalized to Nyquist in [-1.0, 1.0).
            rate: float - in [0.0, 1.0].
        """

        if (frequency < -1.0) or (frequency > 1.0):
            raise ValueError(f"Frequency = {frequency} Expected Frequency in [-1.0, 1.0]")
        if (rate < 0.0) or (rate > 1.0):
            raise ValueError(f"Rate = {rate} Expected Rate in [0.0, 1.0]")
        super().__init__(b=numpy.array([numpy.finfo(float).eps + 0j]), s=numpy.zeros(1, complex))
        self._filter = ComplexExponentialFilter()
        self._frequency = frequency
        self._rate = rate

    def filter(  # type: ignore
        self, d: list | numpy.ndarray
    ) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]:
        """Filters a primary signal and produces a reference signal.

        Signals are Hilbert transformed to complex as necessary.

        Arguments:
            d: list | numpy.ndarray - primary signal.

        Returns:
            y: numpy.ndarray - reference signal.
            e: numpy.ndarray - error signal.
            b: numpy.ndarray - forward coefficient.
        """

        if not isinstance(d, numpy.ndarray):
            d = numpy.array(list(d))
        if not len(d):
            raise ValueError(f"D = {d}")
        if not numpy.iscomplex(d).any():
            d = scipy.signal.hilbert(d)
        x = self._filter.filter(numpy.ones(len(d)) * self.frequency)
        y, e, b = (
            numpy.zeros(len(x), complex),
            numpy.zeros(len(x), complex),
            numpy.zeros(len(x), complex),
        )
        for ii in range(0, len(x)):
            y[ii] = x[ii] * self.b[0]
            e[ii] = d[ii] - y[ii]
            b[ii] = self.b[0]
            self.b[0] += self.rate * e[ii] * numpy.conjugate(x[ii])
        return y, e, b
