""" **Description**

        Phase interface.

    **Example**

        ::

            from diamondback.interfaces.IPhase import IPhase


            class Test( IPhase ) :

                def __init__( self ) :

                    super( ).__init__( )

                    self.phase = 0.0

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-31.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import numpy


class IPhase( IEqual ) :

    """ Phase interface.
    """

    @property
    def phase( self ) :

        """ Normalized phase relative to pi in [ -1.0, 1.0 ] ( float ).
        """

        return self._phase

    @phase.setter
    def phase( self, phase ) :

        if ( ( phase < -1.0 ) or ( phase > 1.0 ) ) :

            raise ValueError( 'Phase = ' + str( phase ) )

        self._phase = phase

    def __eq__( self, other ) :

        """ Evaluates equality condition.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.isclose( self.phase, other.phase ) ) )

    def __init__( self ) :

        """ Initializes an instance.
        """

        super( ).__init__( )

        self._phase = 0.0
