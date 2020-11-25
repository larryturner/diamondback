""" **Description**

        Proxy interface.

    **Example**

        ::

            from diamondback import IProxy


            class Test( IProxy ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.proxy = { 'http' : 'http://proxy.net:9480', 'https' : 'https://proxy.net:8080' }


            test = Test( )

            test.proxy[ 'http' ] = 'http://proxy.net:80'

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2020, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-09-25.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import typing


class IProxy( IEqual ) :

    """ Proxy interface.
    """

    @property
    def proxy( self ) :

        """ Proxy ( dict( str, str ) ).
        """

        return self._proxy

    @proxy.setter
    def proxy( self, proxy : typing.Dict[ str, str ] ) :

        self._proxy = proxy

    def __eq__( self, other : any ) -> bool :

        """ Equality.

            Arguments :

                other - Other ( any ).

            Returns :

                equality - Equality ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.proxy == other.proxy ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._proxy = { }
