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

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-31.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
from typing import Any, List, Union
import numpy

class IS( IEqual ) :

    """ State interface.
    """

    @property
    def s( self ) :

        """ s : Union[ List, numpy.ndarray ] - state.
        """

        return self._s

    @s.setter
    def s( self, s : Union[ List, numpy.ndarray ] ) :

        self._s = s

    def __eq__( self, other : Any ) -> bool :

        """ Equal.

            Arguments :

                other : Any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.allclose( self.s, other.s ) ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._s = None
