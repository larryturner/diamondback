""" **Description**
        Identity interface.

    **Example**
        ::
            from diamondback import IIdentity
            import uuid

            class Test( IIdentity ) :

                def __init__( self ) -> None :
                    super( ).__init__( )
                    self.identity = str( uuid.uuid4( ) )

            test = Test( )
            test.identity

    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, Analytics & AI, 2020-09-23.
"""

class IIdentity( object ) :

    """ Identity interface.
    """

    @property
    def identity( self ) :

        """ identity : str.
        """

        return self._identity

    @identity.setter
    def identity( self, identity : str ) :

        self._identity = identity

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )
        self._identity = ''
