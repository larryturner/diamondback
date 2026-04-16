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

from diamondback import PidFilter


class TestPidFilter(object):
    """Test PidFilter."""

    def test_init(self):
        """Test init."""

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
