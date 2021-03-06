""" **Description**

        Url interface.

    **Example**

        ::

            from diamondback import IUrl


            class Test( IUrl ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.url = 'http://127.0.0.1:80/service'

            test = Test( )

            test.url = 'http://10.0.0.1:8080/service'

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2020, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-09-25.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual


class IUrl( IEqual ) :

    """ Url interface.
    """

    @property
    def url( self ) :

        """ Url ( str ).
        """

        return self._url

    @url.setter
    def url( self, url : str ) :

        url = url.strip( '/' )

        if ( not url ) :

            raise ValueError( 'Url = ' + str( url ) )

        self._url = url

    def __eq__( self, other : any ) -> bool :

        """ Equality.

            Arguments :

                other - Other ( any ).

            Returns :

                equality - Equality ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.url == other.url ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._url = 'http://127.0.0.1:8080'
