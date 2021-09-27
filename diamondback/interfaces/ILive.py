""" **Description**
        Live interface.

    **Example**
        ::
            from diamondback import ILive

            class Test( ILive ) :

                def __init__( self ) -> None :
                    super( ).__init__( )
                    self.live = False

            test = Test( )
            test.live = True

    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, Analytics & AI, 2021-01-12.
"""

class ILive( object ) :

    """ Live interface.
    """

    @property
    def live( self ) :

        """ live : bool.
        """

        return self._live

    @live.setter
    def live( self, live : bool ) :

        self._live = live

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )
        self._live = False
