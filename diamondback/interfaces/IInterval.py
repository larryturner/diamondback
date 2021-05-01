""" **Description**

        Interval interface.

    **Example**

        ::

            from diamondback import IInterval


            class Test( IInterval ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.interval = 0.0

            test = Test( )

            test.interval = 7200.0

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-07-12.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import numpy
import typing


class IInterval( IEqual ) :

    """ Interval interface.
    """

    @property
    def interval( self ) :

        """ interval : float - in seconds in [ 0.0, inf ).
        """

        return self._interval

    @interval.setter
    def interval( self, interval : float ) :

        if ( interval < 0.0 ) :

            raise ValueError( f'Interval = {interval}' )

        self._interval = interval

    def __eq__( self, other : typing.Any ) -> bool :

        """ Equal.

            Arguments :

                other : typing.Any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.isclose( self.interval, other.interval ) ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._interval = 0.0
