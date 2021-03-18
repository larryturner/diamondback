""" **Description**

        Configure interface.

    **Example**

        ::

            from diamondback import IConfigure


            class Test( IConfigure ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.configure = [ ]

            test = Test( )

            test.configure = { 'a' : 0.0, 'b' : 1.0 }

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-10-27.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual


class IConfigure( IEqual ) :

    """ Configure interface.
    """

    @property
    def configure( self ) :

        """ Configure ( any ).
        """

        return self._configure

    @configure.setter
    def configure( self, configure : any ) :

        self._configure = configure

    def __eq__( self, other : any ) -> bool :

        """ Equal.

            Arguments :

                other - Other ( any ).

            Returns :

                equality - Equality ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.configure == other.configure ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._configure = [ ]
