""" **Description**

        Valid interface.

    **Example**

        ::

            from diamondback.interfaces.IValid import IValid


            class Test( IValid ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.valid = False

            test = Test( )

            test.valid = True

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2020, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-10-22.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual


class IValid( IEqual ) :

    """ Valid interface.
    """

    @property
    def valid( self ) :

        """ Valid ( any ).
        """

        return self._valid

    @valid.setter
    def valid( self, valid : any ) :

        self._valid = valid

    def __eq__( self, other : any ) -> bool :

        """ Evaluates equality condition.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.valid == other.valid ) )

    def __init__( self ) -> None :

        """ Initializes an instance.
        """

        super( ).__init__( )

        self._valid = [ ]
