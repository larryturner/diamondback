""" **Description**

        Proxy interface.

    **Example**

        ::

            from diamondback.interfaces.IProxy import IProxy


            class Test( IProxy ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.proxy = 'https://gateway.schneider.zscaler.net:9480'

            test = Test( )

            test.proxy = 'https://gateway.schneider.zscaler.net:80'

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2020, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-09-25.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual


class IProxy( IEqual ) :

    """ Proxy interface.
    """

    @property
    def proxy( self ) :

        """ Proxy ( str ).
        """

        return self._proxy

    @proxy.setter
    def proxy( self, proxy ) :

        self._proxy = proxy

    def __eq__( self, other : any ) -> bool :

        """ Evaluates equality condition.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.proxy == other.proxy ) )

    def __init__( self ) -> None :

        """ Initializes an instance.
        """

        super( ).__init__( )

        self._proxy = ''
