""" **Description**

    REST client for simple REST service requests.  An API and an elective
    dictionary of parameter strings are encoded to build a URL, elective
    JSON or binary data are defined in the body of a request, and a JSON
    or binary data response is returned and decoded.

    A client instance may be useful as a base client definition to interact
    with a service which satisfies flexible request constraints.

    Caching may be useful in environments with intermittent or inconsistent
    network connectivity.  If caching is specified, requests are cached when
    a service is not live, and sent in order during a subsequent request when
    a service is live.

    URL and proxy definition is supported.

    Thread safe.

    **Example**

        ::

            from diamondback import RestClient
            import typing


            class TestClient( RestClient ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.proxy = { 'http' : '', 'https' : '' }

                def add( self, item : typing.Dict[ str, float ] ) -> float :

                    return self.request( 'get', 'test/add', item = item )

            client = TestClient( )

            client.url = 'http://127.0.0.1:8080'

            client.timeout = ( 10.0, 60.0 )  # connect, read

            client.add( { 'x', 2.71827, 'y' : 3.14159 } )

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2020, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-10-22.

    **Definition**

"""

from diamondback.interfaces.IClear import IClear
from diamondback.interfaces.IData import IData
from diamondback.interfaces.ILive import ILive
from diamondback.interfaces.IProxy import IProxy
from diamondback.interfaces.IReady import IReady
from diamondback.interfaces.ITimeOut import ITimeOut
from diamondback.interfaces.IUrl import IUrl
from diamondback.interfaces.IVersion import IVersion
from threading import RLock
import requests
import typing


class RestClient( IClear, IData, ILive, IProxy, IReady, ITimeOut, IUrl, IVersion ) :

    """ REST client.
    """

    @ILive.live.getter
    def live( self ) :

        """ Live ( bool ).
        """

        try :

            requests.request( method = 'head', url = self.url, proxies = self.proxy, timeout = self.timeout )

            value = True

        except :

            value = False

        return value

    @IReady.ready.getter
    def ready( self ) :

        """ Ready ( bool ).
        """

        try :

            value = requests.request( method = 'get', url = self.url + '/ready', proxies = self.proxy, timeout = self.timeout ).json( )

        except :

            value = False

        return value

    @IVersion.version.getter
    def version( self ) :

        """ Version ( str ).
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

        self._rlock = RLock( )

        self.data = [ ]

        self.proxy, self.timeout = { }, ( 10.0, 60.0 )

        self.url = 'http://127.0.0.1:8080'

    def clear( self ) -> None :

        """ Clear cached requests.
        """

        with ( self._rlock ) :

            self.data = [ ]

    def request( self, method : str, api : str, item : typing.Dict[ str, str ] = None, json : any = None, data : any = None, cache : bool = False ) -> any :

        """ Request client for simple REST service requests. An API and an
            elective dictionary of parameter strings are encoded to build a
            URL, elective JSON or binary data are defined in the body of a
            request, and a JSON or binary data response is returned and
            decoded.  Caching may be useful in environments with intermittent
            or inconsistent network connectivity.  If caching is specified,
            requests are cached when a service is not live, and sent in order
            during a subsequent request when a service is live.

            Arguments :

                method - Method ( str ) in ( 'delete', 'get', 'head', 'options', 'patch', 'post', 'put' ).

                api - API, relative to the URL ( str ).

                item - Item ( dict( str, str ) ).

                json - JSON ( any ).

                data - Data ( any ).

                cache - Cache ( bool ).

            Returns :

                value - Value ( any ).

        """

        if ( not method ) :

            raise ValueError( f'Method = { method }' )

        method = method.lower( )

        if ( method not in ( 'delete', 'get', 'head', 'options', 'patch', 'post', 'put' ) ) :

            raise ValueError( f'Method = { method }' )

        if ( ( data ) and ( json ) ) :

            raise ValueError( f'Data = { data } JSON = { json }' )

        api = api.strip( '/' )

        url = self.url

        if ( api ) :

            url += '/' + api

        valid, value = True, True

        with ( self._rlock ) :

            if ( cache ) :

                if ( not self.live ) :

                    self.data.append( { 'method' : method, 'url' : url, 'item' : item, 'data' : data, 'json' : json } )

                    valid = False

            if ( valid ) :

                if ( self.data ) :

                    if ( self.live ) :

                        for x in [ x for x in self.data ] :

                            try :

                                with requests.request( method = x[ 'method' ], url = x[ 'url' ], params = x[ 'item' ], data = x[ 'data' ], json = x[ 'json' ], proxies = self.proxy, timeout = self.timeout ) as value :

                                    if ( ( not value ) or ( value.status_code != 200 ) ) :

                                        raise ConnectionError( f'Status = { value.status_code } Reason = { value.reason }' )

                            finally :

                                del self.data[ 0 ]

                with requests.request( method = method, url = url, params = item, data = data, json = json, proxies = self.proxy, timeout = self.timeout ) as value :

                    if ( ( not value ) or ( value.status_code != 200 ) ) :

                        raise ConnectionError( f'Status = { value.status_code } Reason = { value.reason }' )

                    try :

                        value = value.json( )

                    except :

                        value = value.content

        return value
