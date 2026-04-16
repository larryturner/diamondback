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

import io
import sys

import numpy

from diamondback import Log


class TestLog(object):
    """Test Log."""

    def test_init(self):
        """Test init."""

        x = [str(x) for x in numpy.random.rand(3)]
        fio = io.StringIO()
        Log.stream(fio)
        Log.level("Critical")
        Log.write("Debug", f"{numpy.random.rand(3) + 1.0}")
        Log.level("Debug")
        Log.write("Info", x[0])
        Log.level("Error")
        Log.write("Warning", f"{numpy.random.rand(3) + 1.0}")
        Log.write("Critical", x[1])
        Log.write("Error", x[2])
        value = fio.getvalue()
        Log.stream(sys.stdout)
        Log.level("Info")
        assert value
        assert value.find(x[0]) > 0
        assert value.find(x[1]) > value.find(x[0])
        assert value.find(x[2]) > value.find(x[1])
