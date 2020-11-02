""" **Description**

        Recursive coefficient interface.

    **Example**

        ::

            from diamondback.interfaces.IA import IA
            import numpy


            class Test( IA ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.a = numpy.array( [ 0.0, 0.1 ] )

            test = Test( )

            test.a[ : ] = 0.0

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-31.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import numpy


class IA( IEqual ) :

    """ Recursive coefficient interface.
    """

    @property
    def a( self ) :

        """ Recursive coefficient ( array( complex | float ) ).
        """

        return self._a

    @a.setter
    def a( self, a : any ) :

        self._a = a

    def __eq__( self, other : any ) -> bool :

        """ Equality.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.allclose( self.a, other.a ) ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._a = [ ]
