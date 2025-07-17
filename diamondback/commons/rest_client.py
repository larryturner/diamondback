"""**Description**
    REST client instances define a client for simple REST service requests
    using the requests package.  An API and an elective dictionary of parameter
    strings are encoded to build a URL, elective binary or JSON data are
    defined in the body of a request, and a requests response containing JSON,
    text, or binary data is returned.

    Proxy, timeout, and URL definition are supported.

    Live makes a head request to a URL and detects a live service.

**Example**

    .. code-block:: python

        from diamondback import RestClient
        import numpy

        class TestClient(RestClient) :

            def __init__(self) -> None :
                super().__init__()
                self.proxy = dict(http = "", https = "")

            def add(self, json : dict[str, numpy.ndarray]) -> numpy.ndarray:
                return self.request("get", "test/add", json = json).json()

        client = TestClient()
        client.url = "http://127.0.0.1:8080"
        client.timeout = (10.0, 60.0)  # connect, read
        value = client.add(dict(x = numpy.random.rand(3), y = numpy.random.rand(3)))

**License**
    `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
    © 2018 - 2025 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

**Author**
    Larry Turner, Schneider Electric, AI Hub, 2020-10-22.
"""

from typing import Any
import requests


class RestClient(object):
    """REST client."""

    METHOD = ("Delete", "Get", "Head", "Options", "Patch", "Post", "Put")

    @property
    def live(self):
        try:
            requests.request(method="head", url=self.url, proxies=self.proxy, timeout=self.timeout)
            value = True
        except Exception:
            value = False
        return value

    @property
    def proxy(self):
        return self._proxy

    @proxy.setter
    def proxy(self, proxy: dict[str, str]):
        self._proxy = proxy

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, timeout: Any):
        self._timeout = timeout

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url: str):
        if url:
            url = url.strip("/")
        self._url = url

    def __init__(self) -> None:
        """Initialize."""

        super().__init__()
        self._proxy = dict()
        self._timeout = (10.0, 60.0)
        self._url = "http://127.0.0.1:8080"

    def request(
        self,
        method: str,
        api: str,
        auth: Any = None,
        header: dict[str, str] | None = None,
        item: dict[str, str] | None = None,
        data: Any = None,
        json: Any = None,
    ) -> requests.Response:
        """Request client for simple REST service requests. An API and an
        elective dictionary of parameter strings are encoded to build a
        URL, elective binary or JSON data are defined in the body of a
        request, and a requests response containing JSON, text, or binary
        data is returned.

        Arguments :
            method : str - in ("delete", "get", "head", "options", "patch", "post", "put").
            api : str - relative to the URL.
            auth : Any.
            header : dict[str, str] | None.
            item : dict[str, str] | None.
            data : Any.
            json : Any.

        Returns :
            value : requests.Response.
        """

        method = method.title()
        if method not in RestClient.METHOD:
            raise ValueError(f"Method = {method} Expected Method in {RestClient.METHOD}")
        if (data) and (json):
            raise ValueError(f"Data = {data} JSON = {json} Expected Data or JSON")
        api = api.strip("/")
        url = self.url
        if api:
            url += "/" + api
        with requests.request(
            method=method,
            url=url,
            params=item,
            data=data,
            headers=header,
            auth=auth,
            json=json,
            proxies=self.proxy,
            timeout=self.timeout,
        ) as value:
            value.raise_for_status()
        return value
