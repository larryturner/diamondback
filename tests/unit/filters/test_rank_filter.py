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

import numpy

from diamondback import RankFilter


class TestRankFilter(object):
    """Test RankFilter."""

    def test_init(self):
        """Test init."""

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
