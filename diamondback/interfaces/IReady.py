""" **Description**

        Ready interface.

    **Example**

        ::

            from diamondback import IReady


            class Test( IReady ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.ready = False

            test = Test( )

            test.ready = True

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2021-01-12.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual


class IReady( IEqual ) :

    """ Ready interface.
    """

    @property
    def ready( self ) :

        """ ready : any.
        """

        return self._ready

    @ready.setter
    def ready( self, ready : any ) :

        self._ready = ready

    def __eq__( self, other : any ) -> bool :

        """ Equal.

            Arguments :

                other : any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( self.ready == other.ready ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._ready = None
