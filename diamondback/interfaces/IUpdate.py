""" **Description**

        Update interface.

    **Example**

        ::

            from diamondback.interfaces.IPhase
            from diamondback.interfaces.IUpdate


            class Test( IPhase, IUpdate ) :

                def update( self ) -> None :

                    self.phase += 1.0

            test = Test( )

            test.update( )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-03-23.

    **Definition**

"""

from abc import ABC, abstractmethod


class IUpdate( ABC ) :

    """ Update interface.
    """

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

    @abstractmethod
    def update( self ) -> None :

        """ Update.
        """

        pass

