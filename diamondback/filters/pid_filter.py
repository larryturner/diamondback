"""**Description**
    A Proportional Integral Derivative (PID) filter realizes a discrete
    difference equation as a function of a forward coefficient array and a
    state array of a static order.  A forward coefficient array applies a
    gain to proportional, integral, and derivative representations of an
    incident signal, producing a reference signal.  An integral limit is
    specified, preventing integral saturation which may adversely affect
    control stability and latency.

    .. math::

        y_{n} = b_{0}\\ x_{n} + b_{1}\\max(\\min(\\sum_{0}^{n}\\ x_{n},\\ limit\\ ),\\ -limit) + b_{2}\\ \\frac{d}{dn}(\\ x_{n})

**Example**

    .. code-block:: python

        from diamondback import ComplexExponentialFilter, PidFilter
        import numpy

        pid_filter = PidFilter(b = numpy.array([0.1, 5.0e-2, 0.0]))
        x = ComplexExponentialFilter(0.0).filter(numpy.linspace(-1.0e-4, 1.0e-4, 128) * 0.1).real
        y = pid_filter.filter(x)

**License**
    `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
    © 2018 - 2025 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

**Author**
    Larry Turner, Schneider Electric, AI Hub, 2018-01-31.
"""

from diamondback.filters.fir_filter import FirFilter
import numpy


class PidFilter(FirFilter):
    """Proportional Integral Derivative (PID) filter."""

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, limit: float):
        if limit < 0.0:
            raise ValueError(f"Limit = {limit} Expected Limit in (0.0, inf)")
        self._limit = limit

    def __init__(self, b: list | numpy.ndarray) -> None:
        """Initialize.

        Arguments:
            b: list | numpy.ndarray - forward coefficient.
        """

        if not isinstance(b, numpy.ndarray):
            b = numpy.array(list(b))
        if len(b) != 3:
            raise ValueError(f"B = {b}")
        super().__init__(b=b, s=numpy.zeros(len(b)))
        self._limit = numpy.inf

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
            self.s[2] = x[ii] - self.s[0]
            if abs(self.s[1] + x[ii]) < self.limit:
                self.s[1] += x[ii]
            self.s[0] = x[ii]
            y[ii] = self.b.dot(self.s)
        return y
