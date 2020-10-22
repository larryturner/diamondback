""" **Description**

        Reset interface.

    **Example**

        ::

            from diamondback.interfaces.IReset import IReset
            from diamondback.interfaces.IPhase import IS
            import numpy


            class Test( IReset, IS ) :

                def reset( self, x : any ) -> None :

                    self.s[ : ] = x

            test = Test( )

            test.s = numpy.array( [ 0.0, 1.0 ] )

            test.reset( 0.5 )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-03-12.

    **Definition**

"""

from abc import ABC, abstractmethod


class IReset( ABC ) :

    """ Reset interface.
    """

    def __init__( self ) -> None :

        """ Initializes an instance.
        """

        super( ).__init__( )

    @abstractmethod
    def reset( self, x : any ) -> None :

        """ Modifies a state to minimize edge effects by assuming persistent
            operation at a specified incident signal condition.

            Arguments :

                x - Incident signal ( complex, float ).
        """

        pass

