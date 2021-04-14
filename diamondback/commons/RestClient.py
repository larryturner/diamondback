""" **Description**

    REST client instances define a client for simple REST service requests
    using the requests package.  An API and an elective dictionary of parameter
    strings are encoded to build a URL, elective JSON or binary data are
    defined in the body of a request, and a requests response containing JSON,
    text, or binary data is returned.

    Proxy, timeout, and URL definition are supported.

    Live makes a head request to a URL and detects a live service.

    Ready makes a get request to a ready API and a service may respond with
    an indication that it is in a condition which supports normal function.

    Version makes a get request to a version API and a service may respond
    with a version string.

    **Example**

        ::

            from diamondback import RestClient
            import numpy
            import typing


            class TestClient( RestClient ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.proxy = { 'http' : '', 'https' : '' }

                def add( self, json : typing.Union[ numpy.ndarray, typing.List[ float ] ] ) -> float :

                    return self.request( 'get', 'test/add', json = json ).json( )

            client = TestClient( )

            client.url = 'http://127.0.0.1:8080'

            client.timeout = ( 10.0, 60.0 )  # connect, read

            client.add( [ 2.71827, 3.14159 ] )

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-10-22.

    **Definition**

"""

from diamondback.interfaces.ILive import ILive
from diamondback.interfaces.IProxy import IProxy
from diamondback.interfaces.IReady import IReady
from diamondback.interfaces.ITimeOut import ITimeOut
from diamondback.interfaces.IUrl import IUrl
from diamondback.interfaces.IVersion import IVersion
import requests
import typing


class RestClient( ILive, IProxy, IReady, ITimeOut, IUrl, IVersion ) :

    """ REST client.
    """

    @ILive.live.getter
    def live( self ) :

        """ live : bool.
        """

        try :

            requests.request( method = 'head', url = self.url, proxies = self.proxy, timeout = self.timeout )

            value = True

        except :

            value = False

        return value

    @IReady.ready.getter
    def ready( self ) :

        """ ready : bool.
        """

        try :

            value = requests.request( method = 'get', url = self.url + '/ready', proxies = self.proxy, timeout = self.timeout ).json( )

        except :

            value = False

        return value

    @IVersion.version.getter
    def version( self ) :

        """ version : str.
        """

        try :

            value = requests.request( method = 'get', url = self.url + '/version', proxies = self.proxy, timeout = self.timeout ).json( )

        except :

            value = ''

        return value

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self.proxy, self.timeout = { }, ( 10.0, 60.0 )

        self.url = 'http://127.0.0.1:8080'

    def request( self, method : str, api : str, item : typing.Dict[ str, str ] = None, json : any = None, data : any = None ) -> requests.Response :

        """ Request client for simple REST service requests. An API and an
            elective dictionary of parameter strings are encoded to build a
            URL, elective JSON or binary data are defined in the body of a
            request, and a requests response containing JSON, text, or binary
            data is returned.

            Arguments :

                method : str - in ( 'delete', 'get', 'head', 'options', 'patch', 'post', 'put' ).

                api : str - relative to the URL.

                item : typing.Dict[ str, str ].

                json : any.

                data : any.

            Returns :

                value : requests.Response.
        """

        if ( not method ) :

            raise ValueError( f'Method = {method}' )

        method = method.lower( )

        if ( method not in ( 'delete', 'get', 'head', 'options', 'patch', 'post', 'put' ) ) :

            raise ValueError( f'Method = {method}' )

        if ( ( data ) and ( json ) ) :

            raise ValueError( f'Data = {data} JSON = {json}' )

        api = api.strip( '/' )

        url = self.url

        if ( api ) :

            url += '/' + api

        with requests.request( method = method, url = url, params = item, data = data, json = json, proxies = self.proxy, timeout = self.timeout ) as value :

            value.raise_for_status( )

        return value
