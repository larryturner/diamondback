""" **Description**
        Url interface.

    **Example**
        ::
            from diamondback import IUrl

            class Test( IUrl ) :

                def __init__( self ) -> None :
                    super( ).__init__( )
                    self.url = 'http://127.0.0.1:8080/service'

            test = Test( )
            test.url = 'http://10.0.0.1:8080/service'

    **License**
        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, Analytics & AI, 2020-09-25.
"""

class IUrl( object ) :

    """ Url interface.
    """

    @property
    def url( self ) :

        """ url : str.
        """

        return self._url

    @url.setter
    def url( self, url : str ) :

        """ Url.
        """

        if ( url ) :
            url = url.strip( '/' )
        self._url = url

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )
        self._url = 'http://127.0.0.1:8080'
