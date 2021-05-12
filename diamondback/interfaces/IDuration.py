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

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-07-12.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import numpy
import typing

class IDuration( IEqual ) :

    """ Duration interface.
    """

    @property
    def duration( self ) :

        """ duration : float - in seconds in [ 0.0, inf ).
        """

        return self._duration

    @duration.setter
    def duration( self, duration : float ) :

        if ( duration < 0.0 ) :

            raise ValueError( f'Duration = {duration}' )

        self._duration = duration

    def __eq__( self, other : typing.Any ) -> bool :

        """ Equal.

            Arguments :

                other : typing.Any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.isclose( self.duration, other.duration ) ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._duration = 0.0
