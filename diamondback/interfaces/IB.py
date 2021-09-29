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
        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-31.
"""

from typing import Any, List, Union
import numpy

class IB( object ) :

    """ Forward coefficient interface.
    """

    @property
    def b( self ) :

        """ b : Union[ List, numpy.ndarray ] - forward coefficient.
        """

        return self._b

    @b.setter
    def b( self, b : Union[ List, numpy.ndarray ] ) :

        self._b = b

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )
        self._b = [ ]
