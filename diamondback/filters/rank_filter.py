"""**Description**
    A rank filter realizes a nonlinear morphological operator consuming an
    incident signal, sorting, indexing, and selecting over a sliding window
    of a specified order, and producing a reference signal.

    Morphological operations include dilation, which defines a rank index
    equal to zero, erosion, which defines a rank index equal to order,
    and median, which defines a rank index equal to order divided by two
    for even order.  Compound morphological operations include close,
    consisting of sequential dilation and erosion, and open, consisting of
    sequential erosion and dilation.  An order and rank are specified.

    .. math::

        y_{n} = sort(\\ x_{n-N+1\\ :\\ n}\\ )[\\ i\\ ]

**Example**

    .. code-block:: python

        from diamondback import RankFilter
        import numpy

        rank_filter = RankFilter(rank = 4, order = 4)
        x = numpy.concatenate((numpy.ones(1), numpy.zeros(10), numpy.ones(4), numpy.zeros(2), numpy.ones(5), numpy.zeros(6)))
        rank_filter.reset(x[0])
        y = rank_filter.filter(x)

**License**
    `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
    © 2018 - 2025 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

**Author**
    Larry Turner, Schneider Electric, AI Hub, 2018-01-31.
"""

from diamondback.filters.fir_filter import FirFilter
import numpy


class RankFilter(FirFilter):
    """Rank filter."""

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index: int):
        if (index < 0) or (index > (len(self.s) - 1)):
            raise ValueError(f"Index = {index} Expected Index in [0, {len(self.s) - 1}]")
        self._index = index

    def __init__(self, index: int, order: int) -> None:
        """Initialize.

        Arguments :
            index : int - in [0, order].
            order : int.
        """

        if (index < 0) or (index > order):
            raise ValueError(f"Index = {index} Order = {order} Expected Index in [0, {order}]")
        super().__init__(b=numpy.ones(order + 1) / (order + 1))
        self._index = index

    def filter(self, x: list | numpy.ndarray) -> numpy.ndarray:
        """Filters an incident signal and produces a reference signal.

        Arguments :
            x : list | numpy.ndarray - incident signal.

        Returns :
            y : numpy.ndarray - reference signal.
        """

        if not isinstance(x, numpy.ndarray):
            x = numpy.array(list(x))
        if not len(x):
            raise ValueError(f"X = {x}")
        y = numpy.zeros(len(x), type(x[0]))
        for ii in range(0, len(x)):
            self.s[0] = x[ii]
            y[ii] = self.s[numpy.argsort(abs(self.s))][self.index]
            if len(self.s) > 1:
                self.s[1:] = self.s[:-1]
        return y
