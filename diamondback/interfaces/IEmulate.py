""" **Description**

        Emulate interface.

    **Example**

        ::

            from diamondback.interfaces.IEmulate import IEmulate


            class Test( IEmulate ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.emulate = False

            test = Test( )

            test.emulate = True

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2020, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-10-15.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual


class IEmulate( IEqual ) :

    """ Emulate interface.
    """

    @property
    def emulate( self ) :

        """ Emulate ( any ).
        """

        return self._emulate

    @emulate.setter
    def emulate( self, emulate : any ) :

        self._emulate = emulate

    def __eq__( self, other : any ) -> bool :

        """ Evaluates equality condition.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.emulate == other.emulate ) )

    def __init__( self ) -> None :

        """ Initializes an instance.
        """

        super( ).__init__( )

        self._emulate = [ ]
