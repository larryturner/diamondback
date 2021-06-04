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

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-09-25.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
from typing import Any, Dict

class IProxy( IEqual ) :

    """ Proxy interface.
    """

    @property
    def proxy( self ) :

        """ proxy : Dict[ str, str ].
        """

        return self._proxy

    @proxy.setter
    def proxy( self, proxy : Dict[ str, str ] ) :

        self._proxy = proxy

    def __eq__( self, other : Any ) -> bool :

        """ Equal.

            Arguments :

                other : Any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( self.proxy == other.proxy ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._proxy = { }
