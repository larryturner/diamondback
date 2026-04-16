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

from diamondback import WindowFilter


class TestWindowFilter(object):
    """Test WindowFilter."""

    def test_init(self):
        """Test init."""

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
