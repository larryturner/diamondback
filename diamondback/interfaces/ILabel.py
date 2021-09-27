""" **Description**
        Label interface.

    **Example**
        ::
            from diamondback import ILabel

            class Test( ILabel ) :

                def __init__( self ) -> None :
                    super( ).__init__( )
                    self.label = ''

            test = Test( )
            test.label = 'label'

    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, Analytics & AI, 2021-03-15.

    **Definition**
"""

from diamondback.interfaces.IEqual import IEqual
from typing import Any

class ILabel( IEqual ) :

    """ Label interface.
    """

    @property
    def label( self ) :

        """ label : str.
        """

        return self._label

    @label.setter
    def label( self, label : str ) :

        self._label = label

    def __eq__( self, other : Any ) -> bool :

        """ Equal.

            Arguments :
                other : Any.

            Returns :
                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( self.label == other.label ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )
        self._label = ''
