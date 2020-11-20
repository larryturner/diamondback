""" **Description**

        Clear interface.

    **Example**

        ::

            from diamondback import IClear, IPhase


            class Test( IClear, IPhase ) :

                def clear( self ) -> None :

                    self.phase = 0.0

            test = Test( )

            test.clear( )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2019, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2019-01-25.

    **Definition**

"""

from abc import ABC, abstractmethod


class IClear( ABC ) :

    """ Clear interface.
    """

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

    @abstractmethod
    def clear( self ) -> None :

        """ Clears an instance.
        """

        pass

