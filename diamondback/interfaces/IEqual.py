""" **Description**

        Equal interface.

    **Example**

        ::

            from diamondback import IEqual, IPhase


            class Test( IEqual, IPhase ) :

                def __eq__( self, other : any ) -> bool :

                    return ( ( super( ).__eq__( other ) ) and ( numpy.isclose( self.phase, other.phase ) ) )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-23.

    **Definition**

"""

class IEqual( object ) :

    """ Equal interface.
    """

    def __eq__( self, other : any ) -> bool :

        """ Equal.

            Arguments :

                other : any.

            Returns :

                equal : bool.
        """

        return ( ( isinstance( other, self.__class__ ) ) and ( ( id( self ) == id( other ) ) or ( super( ).__eq__( other ) ) ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        pass

    def __ne__( self, other : any ) -> bool :

        """ Not equal.

            Arguments :

                other : any.

            Returns :

                notequal : bool.
        """

        return not ( self == other )
