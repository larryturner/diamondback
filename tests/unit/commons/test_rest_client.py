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

from diamondback import RestClient


class TestRestClient(object):
    """Test RestClient."""

    def test_init(self):
        """Test init."""

        rest_client = RestClient()
        rest_client.url = "http://marines.com"
        assert rest_client.live
        assert rest_client.request(method="get", api="").content
