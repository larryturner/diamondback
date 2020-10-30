""" **Description**

        Rate interface.

    **Example**

        ::

            from diamondback.interfaces.IRate import IRate


            class Test( IRate ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.rate = 5.0e-2

            test = Test( )

            test.rate = 1.0e-3

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-31.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import numpy


class IRate( IEqual ) :

    """ Rate interface.
    """

    @property
    def rate( self ) :

        """ Rate of adaptation ( float ).
        """

        return self._rate

    @rate.setter
    def rate( self, rate : float ) :

        if ( rate < 0.0 ) :

            raise ValueError( 'Rate = ' + str( rate ) )

        self._rate = rate

    def __eq__( self, other : any ) -> bool :

        """ Equality.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.isclose( self.rate, other.rate ) ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._rate = 0.0
