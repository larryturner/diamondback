""" **Description**

        Equal interface.

    **Example**

        ::

            from diamondback import IEqual, IPhase
            import typing

            class Test( IEqual, IPhase ) :

                def __eq__( self, other : typing.Any ) -> bool :

                    return ( ( super( ).__eq__( other ) ) and ( numpy.isclose( self.phase, other.phase ) ) )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-23.

    **Definition**

"""

import typing

class IEqual( object ) :

    """ Equal interface.
    """

    def __eq__( self, other : typing.Any ) -> bool :

        """ Equal.

            Arguments :

                other : typing.Any.

            Returns :

                equal : bool.
        """

        return ( ( isinstance( other, self.__class__ ) ) and ( ( id( self ) == id( other ) ) or ( super( ).__eq__( other ) ) ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        pass

    def __ne__( self, other : typing.Any ) -> bool :

        """ Not equal.

            Arguments :

                other : typing.Any.

            Returns :

                notequal : bool.
        """

        return not ( self == other )
