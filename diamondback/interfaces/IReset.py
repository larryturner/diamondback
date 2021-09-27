""" **Description**
        Reset interface.

    **Example**
        ::
            from diamondback import IReset, IS
            from typing import Union
            import numpy

            class Test( IReset, IS ) :

                def reset( self, x : Union[ complex, float ] ) -> None :
                    self.s[ : ] = x

            test = Test( )
            test.s = numpy.array( [ 0.0, 1.0 ] )
            test.reset( 0.5 )

    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, Analytics & AI, 2018-03-12.
"""

from abc import ABC, abstractmethod
from typing import Union

class IReset( ABC ) :

    """ Reset interface.
    """

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

    @abstractmethod
    def reset( self, x : Union[ complex, float ] ) -> None :

        """ Modifies a state to minimize edge effects by assuming persistent
            operation at a specified incident signal condition.

            Arguments :
                x : Union[ complex, float ] - incident signal.
        """

        pass

