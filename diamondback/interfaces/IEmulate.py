""" **Description**

        Emulate interface.

    **Example**

        ::

            from diamondback import IEmulate


            class Test( IEmulate ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.emulate = False

            test = Test( )

            test.emulate = True

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-10-15.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import typing


class IEmulate( IEqual ) :

    """ Emulate interface.
    """

    @property
    def emulate( self ) :

        """ emulate : typing.Any.
        """

        return self._emulate

    @emulate.setter
    def emulate( self, emulate : typing.Any ) :

        self._emulate = emulate

    def __eq__( self, other : typing.Any ) -> bool :

        """ Equal.

            Arguments :

                other : typing.Any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( self.emulate == other.emulate ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._emulate = None
