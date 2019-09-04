""" **Description**

        Reset interface.

    **Example**

        ::

            from diamondback.interfaces.IPhase import IPhase
            from diamondback.interfaces.IReset import IReset

            class Test( IPhase, IReset ) :

                def reset( self, x ) :

                    self.phase = x

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

    def __init__( self ) :

        """ Initializes an instance.
        """

        super( ).__init__( )

    @abstractmethod
    def reset( self, x ) :

        """ Modifies a state to minimize edge effects by assuming persistent
            operation at a specified incident signal condition.

            Arguments :

                x - Incident signal ( complex, float ).
        """

        pass

