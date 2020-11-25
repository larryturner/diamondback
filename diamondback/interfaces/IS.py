""" **Description**

        State interface.

    **Example**

        ::

            from diamondback import IS
            import numpy


            class Test( IS ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.s = numpy.array( [ 0.0, 0.1 ] )

            test = Test( )

            test.s[ : ] = 0.0

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-31.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import numpy


class IS( IEqual ) :

    """ State interface.
    """

    @property
    def s( self ) :

        """ State ( array( complex | float ) ).
        """

        return self._s

    @s.setter
    def s( self, s : any ) :

        self._s = s

    def __eq__( self, other : any ) -> bool :

        """ Equality.

            Arguments :

                other - Other ( any ).

            Returns :

                equality - Equality ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.allclose( self.s, other.s ) ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._s = [ ]
