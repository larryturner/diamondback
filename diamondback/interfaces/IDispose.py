""" **Description**

        Dispose interface.

    **Example**

        ::

            from diamondback import IDispose


            class Test( IDispose ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.dispose = False

            test = Test( )

            test.dispose = True

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-10-22.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import typing


class IDispose( IEqual ) :

    """ Dispose interface.
    """

    @property
    def dispose( self ) :

        """ dispose : typing.Any.
        """

        return self._dispose

    @dispose.setter
    def dispose( self, dispose : typing.Any ) :

        self._dispose = dispose

    def __eq__( self, other : typing.Any ) -> bool :

        """ Equal.

            Arguments :

                other : typing.Any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( self.dispose == other.dispose ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._dispose = None
