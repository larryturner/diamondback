""" **Description**

        Duration interface.

    **Example**

        ::

            from diamondback import IDuration


            class Test( IDuration ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.duration = 0.0

            test = Test( )

            test.duration = 3600.0

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-07-12.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import numpy


class IDuration( IEqual ) :

    """ Duration interface.
    """

    @property
    def duration( self ) :

        """ Duration in seconds in [ 0.0, inf ) ( float ).
        """

        return self._duration

    @duration.setter
    def duration( self, duration : float ) :

        if ( duration < 0.0 ) :

            raise ValueError( f'Duration = {duration}' )

        self._duration = duration

    def __eq__( self, other : any ) -> bool :

        """ Equal.

            Arguments :

                other - Other ( any ).

            Returns :

                equality - Equality ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.isclose( self.duration, other.duration ) ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._duration = 0.0
