""" **Description**

    REST client for simple REST service requests.  Parameters in a dictionary
    of strings are encoded to build a URL, a request is made, and a JSON
    response is returned and decoded.

    A client instance may be useful as a base client definition to interact
    with a service which satisfies the constraints of parameterized value URL
    encoding, with a JSON response.

    Caching may be useful in environments with intermittent or inconsistent
    network connectivity.  If caching is enabled, delete and put requests are
    cached and sent in order during a later request when the service is not
    ready, a property which may be overriden.

    URL and proxy definition is supported.

    Thread safe and reentrant.

    **Example**

        ::

            from diamondback.clients.RestClient import RestClient
            import requests


            class TestClient( RestClient ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.cache = True

                @property
                def add( self, data ) :

                    return float( self.request( method = requests.get, api = 'test/add', data = data ) )

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
import getpass
import requests
import typing


class RestClient( ICache, IData, IProxy, IUrl ) :

    """ Rest client.
    """

    @property
    def live( self ) :

        """ Live ( bool ).
        """

        return bool( self.request( requests.get, 'live' ) )

    @property
    def ready( self ) :

        """ Ready ( bool ).
        """

        return ( ( self.live ) and ( bool( self.request( requests.get, 'ready' ) ) ) )

    @property
    def user( self ) :

        """ User ( str ).
        """

        return getpass.getuser( )

    def __init__( self ) -> None :

        """ Initializes an instance.
        """

        super( ).__init__( )

        self._rlock = RLock( )

        self.cache, self.data = False, [ ]

        self.proxy, self.url = '', 'http://127.0.0.1:8080'

    def request( self, method : typing.Callable[ [ ], any ], api : str, data : typing.Dict[ str, str ] = None ) -> any :

        """ Request.

            Arguments :

                method - Method ( method ) in ( requests.delete, requests.get, requests.post, requests.put ).

                api - API ( str ).

                data - Data ( dict( str, str ) ).

            Returns :

                value - Value ( any ).

        """

        if ( ( not method ) or ( method not in ( requests.delete, requests.get, requests.post, requests.put ) ) ) :

            raise ValueError( 'Method = ' + str( method ) )

        url = self.url + '/' + api

        if ( data ) :

            url += '?' + '&'.join( [ x + '=' + requests.utils.quote( y ) for ( x, y ) in data.items( ) ] )

        value = True

        with ( self._rlock ) :

            self.data.append( { 'method' : method, 'url' : url } )

            if ( ( not self.cache ) or ( ( method not in ( requests.delete, requests.put ) ) or ( self.ready ) ) ) :

                for x in [ x for x in self.data ] :

                    try :

                        with x[ 'method' ]( url = x[ 'url' ], proxies = { 'http' : self.proxy, 'https' : self.proxy }, timeout = 15.0 ) as value :

                            if ( ( not value ) or ( value.status_code != 200 ) ) :

                                raise ConnectionError( '{:30s}{:30s}'.format( 'Status = ' + str( value.status_code ), 'Reason = ' + str( value.reason ) ) )

                            value = value.json( )

                    finally :

                        del self.data[ 0 ]

        return value
