""" **Description**
        Recursive coefficient interface.

    **Example**
        ::
            from diamondback import IA
            import numpy

            class Test( IA ) :

                def __init__( self ) -> None :
                    super( ).__init__( )
                    self.a = numpy.array( [ 0.0, 0.1 ] )

            test = Test( )
            test.a[ : ] = 0.0

    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-31.
"""

from typing import Any, List, Union
import numpy

class IA( object ) :

    """ Recursive coefficient interface.
    """

    @property
    def a( self ) :

        """ a : Union[ List, numpy.ndarray ] - recursive coefficient.
        """

        return self._a

    @a.setter
    def a( self, a : Union[ List, numpy.ndarray ] ) :

        self._a = a

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )
        self._a = [ ]
