""" **Description**

    REST client for simple REST service requests.  An API and an elective
    dictionary of parameter strings are encoded to build a URL, elective
    JSON or binary data are defined in the body of a request, and a JSON
    or binary response is returned and decoded.

    A client instance may be useful as a base client definition to interact
    with a service which satisfies flexible request constraints.

    Caching may be useful in environments with intermittent or inconsistent
    network connectivity.  If caching is specified, requests are cached when
    a service is not live, and sent in order during a subsequent request when
    a service is live.

    URL and proxy definition is supported.

    Thread safe and reentrant.

    **Example**

        ::

            from diamondback import RestClient
            import requests
            import typing


            class TestClient( RestClient ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

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

from diamondback.interfaces.IData import IData
from diamondback.interfaces.ILive import ILive
from diamondback.interfaces.IProxy import IProxy
from diamondback.interfaces.IReady import IReady
from diamondback.interfaces.IUrl import IUrl
from diamondback.interfaces.IUser import IUser
from diamondback.interfaces.IVersion import IVersion
from threading import RLock
import requests
import typing


class RestClient( IData, ILive, IProxy, IReady, IUrl, IUser, IVersion ) :

    """ REST client.
    """

    @ILive.live.getter
    def live( self ) :

        """ Live ( bool ).
        """

        try :

            requests.request( method = 'get', url = self.url )

            value = True

        except :

            try :

                value = requests.request( method = 'get', url = self.url + '/live' ).json( )

            except :

                value = False

        return value

    @IReady.ready.getter
    def ready( self ) :

        """ Ready ( bool ).
        """

        try :

            value = requests.request( method = 'get', url = self.url + '/ready' ).json( )

        except :

            value = False

        return value

    @IVersion.version.getter
    def version( self ) :

        """ Version ( str ).
        """

        try :

            value = requests.request( method = 'get', url = self.url + '/version' ).json( )

        except :

            value = ''

        return value

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._rlock = RLock( )

        self.data = [ ]

        self.proxy, self.url = { }, 'http://127.0.0.1:8080'

    def request( self, method : str, api : str, item : typing.Dict[ str, str ] = None, json : any = None, data : any = None, cache : bool = False, timeout : typing.Tuple[ float, float ] = ( 15.0, 60.0 ) ) -> any :

        """ Request client for simple REST service requests. An API and an
            elective dictionary of parameter strings are encoded to build a
            URL, elective JSON or binary data are defined in the body of a
            request, and a JSON or binary response is returned and decoded.
            If cache is specified, requests are cached if a service is not
            live.

            Arguments :

                method - Method ( str ) in ( 'delete', 'get', 'head', 'options', 'patch', 'post', 'put' ).

                api - API, relative to the URL ( str ).

                item - Item ( dict( str, str ) ).

                json - JSON ( any ).

                data - Data ( any ).

                cache - Cache ( bool ).

                timeout - Timeout ( tuple( connect : float, read : float ) ).

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

        if ( min( timeout ) <= 0.0 ) :

            raise ValueError( 'Timeout = ' + str( timeout ) )

        api = api.strip( '/' )

        url = self.url

        if ( api ) :

            url += '/' + api

        ready, value = True, True

        with ( self._rlock ) :

            if ( cache ) :

                if ( not self.live ) :

                    self.data.append( { 'method' : method, 'url' : url, 'item' : item, 'data' : data, 'json' : json } )

                    ready = False

            if ( ready ) :

                if ( any( self.data ) ) :

                    if ( self.live ) :

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

                    try :

                        value = value.json( )

                    except :

                        value = value.content

        return value
