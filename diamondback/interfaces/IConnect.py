""" **Description**

        Connect interface.

    **Example**

        ::

            from diamondback import IConnect


            class Test( IConnect ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.connect = { }

            test = Test( )

            test.connect = { 'http' : 'proxy.net:8080' }

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-10-15.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual


class IConnect( IEqual ) :

    """ Connect interface.
    """

    @property
    def connect( self ) :

        """ connect : any.
        """

        return self._connect

    @connect.setter
    def connect( self, connect : any ) :

        self._connect = connect

    def __eq__( self, other : any ) -> bool :

        """ Equal.

            Arguments :

                other : any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( self.connect == other.connect ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._connect = None
