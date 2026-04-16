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

from diamondback import IirFilter, Serial


class TestSerial(object):
    """Test Serial."""

    def test_init(self):
        """Test init."""

        x = IirFilter(style="Butterworth", frequency=0.1, order=4, count=1)
        for compress in (False, True):
            y = Serial.decode(Serial.encode(x, compress))
            assert (numpy.allclose(x.a, y.a)) and (numpy.allclose(x.b, y.b)) and (numpy.allclose(x.s, y.s))
            assert Serial.code(Serial.encode(x, compress=False)) == Serial.code(Serial.encode(y, compress=False))
        x = dict(x=numpy.random.rand(30, 50), y=numpy.random.rand(50, 30))
        for compress in (False, True):
            y = Serial.decode(Serial.encode(x, compress))
            assert Serial.encode(x, compress=False) == Serial.encode(y, compress=False)
            assert all([u in x for u in list(y.keys())])
