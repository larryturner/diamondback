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

        Copyright (c) 2020, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-09-23.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual


class IIdentity( IEqual ) :

    """ Identity interface.
    """

    @property
    def identity( self ) :

        """ identity : any.
        """

        return self._identity

    @identity.setter
    def identity( self, identity : any ) :

        self._identity = identity

    def __eq__( self, other : any ) -> bool :

        """ Equal.

            Arguments :

                other : any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( self.identity == other.identity ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._identity = None
