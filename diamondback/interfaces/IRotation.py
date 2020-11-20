""" **Description**

        Rotation interface.

    **Example**

        ::

            from diamondback import IRotation


            class Test( IRotation ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.rotation = 0.0

            test = Test( )

            test.rotation = 90.0

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2019, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2019-10-09.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import numpy


class IRotation( IEqual ) :

    """ Rotation interface.
    """

    @property
    def rotation( self ) :

        """ Rotation ( float ).
        """

        return self._rotation

    @rotation.setter
    def rotation( self, rotation : float ) :

        self._rotation = rotation

    def __eq__( self, other : any ) -> bool :

        """ Equality.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.isclose( self.rotation, other.rotation ) ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._rotation = 0.0
