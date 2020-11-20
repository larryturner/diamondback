""" **Description**

    REST client for simple REST service requests.  An API and an elective
    dictionary of parameter strings are encoded to build a URL, elective
    JSON or binary data are defined in the body of a request, and a JSON
    response is returned and decoded.

    A client instance may be useful as a base client definition to interact
    with a service which satisfies flexible request constraints.

    Caching may be useful in environments with intermittent or inconsistent
    network connectivity.  If caching is enabled, delete, patch, and put
    requests are cached when a service is not live, and sent in order during
    a subsequent request when a service is live.

    URL and proxy definition is supported.

    Thread safe and reentrant.

    **Example**

        ::

            from diamondback.clients.RestClient import RestClient
            import requests
            import typing


            class TestClient( RestClient ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.cache = False

                    self.proxy = { 'http' : '', 'https' : '' }


                def add( self, item : typing.Dict[ str, float ] ) -> float :

                    return self.request( 'get', api = 'test/add', item = item )

            client = TestClient( )

            client.url = 'http://127.0.0.1:8080'

            client.add( { 'x', 2.71827, 'y' : 3.14159 } )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2020, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-10-22.

    **Definition**

"""

from diamondback.interfaces.ICache import ICache
from diamondback.interfaces.IData import IData
from diamondback.interfaces.IProxy import IProxy
from diamondback.interfaces.IUrl import IUrl
from threading import RLock
import requests
import typing


class RestClient( ICache, IData, IProxy, IUrl ) :

    """ REST client.
    """

    @property
    def live( self ) :

        """ Live ( bool ).
        """

        try :

            value = requests.request( method = 'get', url = self.url, timeout = 15.0 )

            if ( ( value ) and ( value.status_code == 200 ) ) :

                value = True

        except :

            value = False

        return bool( value )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._rlock = RLock( )

        self.cache, self.data = False, [ ]

        self.proxy, self.url = { }, 'http://127.0.0.1:8080'

    def request( self, method : str, api : str, item : typing.Dict[ str, str ] = None, json : any = None, data : any = None, timeout = 15.0 ) -> any :

        """ Request client for simple REST service requests. An API and an
            elective dictionary of parameter strings are encoded to build a
            URL, elective JSON or binary data are defined in the body of a
            request, and a JSON response is returned and decoded.

            Arguments :

                method - Method ( str ) in ( 'delete', 'get', 'head', 'options', 'patch', 'post', 'put' ).

                api - API ( str ).

                item - Item ( dict( str, str ) ).

                json - JSON ( any ).

                data - Data ( any ).

                timeout - Timeout ( float ).

            Returns :

                value - Value ( any ).

        """

        if ( not method ) :

            raise ValueError( 'Method = ' + str( method ) )

        method = method.lower( )

        if ( method not in ( 'delete', 'get', 'head', 'options', 'patch', 'post', 'put' ) ) :

            raise ValueError( 'Method = ' + str( method ) )

        if ( ( data ) and ( json ) ) :

            raise ValueError( '{:30s}{:30s}'.format( 'Data = ' + str( data ), 'Json = ' + str( json ) ) )

        if ( timeout <= 0.0 ) :

            raise ValueError( 'Timeout = ' + str( timeout ) )

        api = api.strip( '/' )

        url = self.url

        if ( api ) :

            url += '/' + api

        value = True

        with ( self._rlock ) :

            cache, live = self.cache, self.live

            if ( ( cache ) and ( not live ) and ( method in ( 'delete', 'patch', 'put' ) ) ) :

                self.data.append( { 'method' : method, 'url' : url, 'item' : item, 'data' : data, 'json' : json } )

            else :

                if ( live ) :

                    for x in [ x for x in self.data ] :

                        try :

                            with requests.request( method = x[ 'method' ], url = x[ 'url' ], params = x[ 'item' ], data = x[ 'data' ], json = x[ 'json' ], proxies = self.proxy, timeout = timeout ) as value :

                                if ( ( not value ) or ( value.status_code != 200 ) ) :

                                    raise ConnectionError( '{:30s}{:30s}'.format( 'Status = ' + str( value.status_code ), 'Reason = ' + str( value.reason ) ) )

                        finally :

                            del self.data[ 0 ]

                with requests.request( method = method, url = url, params = item, data = data, json = json, proxies = self.proxy, timeout = timeout ) as value :

                    if ( ( not value ) or ( value.status_code != 200 ) ) :

                        raise ConnectionError( '{:30s}{:30s}'.format( 'Status = ' + str( value.status_code ), 'Reason = ' + str( value.reason ) ) )

                    value = value.json( )

        return value
