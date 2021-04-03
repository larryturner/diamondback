""" **Description**

        State derivative interface.

    **Example**

        ::

            from diamondback import IQ
            import numpy


            class Test( IQ ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.q = numpy.array( [ 0.0, 0.1 ] )

            test = Test( )

            test.q[ : ] = 0.1

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-31.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import numpy


class IQ( IEqual ) :

    """ State derivative interface.
    """

    @property
    def q( self ) :

        """ q : numpy.ndarray - state derivative.
        """

        return self._q

    @q.setter
    def q( self, q : any ) :

        self._q = q

    def __eq__( self, other : any ) -> bool :

        """ Equal.

            Arguments :

                other : any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.allclose( self.q, other.q ) ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._q = None
