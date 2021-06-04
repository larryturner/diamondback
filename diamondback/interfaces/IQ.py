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

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-31.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
from typing import Any, List, Union
import numpy

class IQ( IEqual ) :

    """ State derivative interface.
    """

    @property
    def q( self ) :

        """ q : Union[ List, numpy.ndarray ] - state derivative.
        """

        return self._q

    @q.setter
    def q( self, q : Union[ List, numpy.ndarray ] ) :

        self._q = q

    def __eq__( self, other : Any ) -> bool :

        """ Equal.

            Arguments :

                other : Any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.allclose( self.q, other.q ) ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._q = None
