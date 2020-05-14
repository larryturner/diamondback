""" **Description**

        Forward coefficient interface.

    **Example**

        ::

            from diamondback.interfaces.IB import IB
            import numpy


            class Test( IB ) :

                def __init__( self ) :

                    super( ).__init__( )

                    self.b = numpy.array( [ 0.75, 0.25 ] )

            test = Test( )

            test.b[ : ] = 0.5

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-31.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import numpy


class IB( IEqual ) :

    """ Forward coefficient interface.
    """

    @property
    def b( self ) :

        """ Forward coefficient ( array( complex | float ) ).
        """

        return self._b

    @b.setter
    def b( self, b ) :

        self._b = b

    def __eq__( self, other ) :

        """ Evaluates equality condition.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.allclose( self.b, other.b ) ) )

    def __init__( self ) :

        """ Initializes an instance.
        """

        super( ).__init__( )

        self._b = [ ]
