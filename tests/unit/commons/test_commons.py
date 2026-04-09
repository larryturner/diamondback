"""**Description**
    Test *diamondback* *commons*.

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
import pytest

from diamondback import IirFilter, Log, RestClient, Serial


class Test(object):
    """Test."""

    def test_Log(self):
        """Test Log."""

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

    def test_RestClient(self):
        """Test RestClient."""

        rest_client = RestClient()
        rest_client.url = "http://marines.com"
        assert rest_client.live
        assert rest_client.request(method="get", api="").content

    def test_Serial(self):
        """Test Serial."""

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
