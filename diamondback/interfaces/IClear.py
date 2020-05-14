""" **Description**

        Clear interface.

    **Example**

        ::

            from diamondback.interfaces.IClear import IClear
            from diamondback.interfaces.IPhase import IPhase


            class Test( IClear, IPhase ) :

                def clear( self ) :

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

    def __init__( self ) :

        """ Initializes an instance.
        """

        super( ).__init__( )

    @abstractmethod
    def clear( self ) :

        """ Clears an instance.
        """

        pass

