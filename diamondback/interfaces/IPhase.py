""" **Description**

        Phase interface.

    **Example**

        ::

            from diamondback import IPhase

            class Test( IPhase ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.phase = 0.0

            test = Test( )

            test.phase = 0.5

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-31.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import numpy
import typing

class IPhase( IEqual ) :

    """ Phase interface.
    """

    @property
    def phase( self ) :

        """ phase : float - relative to pi in [ -1.0, 1.0 ].
        """

        return self._phase

    @phase.setter
    def phase( self, phase : float ) :

        if ( ( phase < -1.0 ) or ( phase > 1.0 ) ) :

            raise ValueError( f'Phase = {phase}' )

        self._phase = phase

    def __eq__( self, other : typing.Any ) -> bool :

        """ Equal.

            Arguments :

                other : typing.Any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.isclose( self.phase, other.phase ) ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._phase = 0.0
