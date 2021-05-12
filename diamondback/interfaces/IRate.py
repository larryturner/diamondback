""" **Description**

        Rate interface.

    **Example**

        ::

            from diamondback import IRate

            class Test( IRate ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.rate = 5.0e-2

            test = Test( )

            test.rate = 1.0e-3

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-31.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import numpy
import typing

class IRate( IEqual ) :

    """ Rate interface.
    """

    @property
    def rate( self ) :

        """ rate : float - in [ 0.0, inf ).
        """

        return self._rate

    @rate.setter
    def rate( self, rate : float ) :

        if ( rate < 0.0 ) :

            raise ValueError( f'Rate = {rate}' )

        self._rate = rate

    def __eq__( self, other : typing.Any ) -> bool :

        """ Equal.

            Arguments :

                other : typing.Any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.isclose( self.rate, other.rate ) ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._rate = 0.0
