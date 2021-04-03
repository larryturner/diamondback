""" **Description**

        Forward coefficient interface.

    **Example**

        ::

            from diamondback import IB
            import numpy


            class Test( IB ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.b = numpy.array( [ 0.75, 0.25 ] )

            test = Test( )

            test.b[ : ] = 0.5

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-31.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import numpy


class IB( IEqual ) :

    """ Forward coefficient interface.
    """

    @property
    def b( self ) :

        """ b : numpy.ndarray - forward coefficient.
        """

        return self._b

    @b.setter
    def b( self, b : any ) :

        self._b = b

    def __eq__( self, other : any ) -> bool :

        """ Equal.

            Arguments :

                other : any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.allclose( self.b, other.b ) ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._b = None
