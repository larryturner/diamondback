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

        Copyright (c) 2021, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2021-03-15.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual


class ILabel( IEqual ) :

    """ Label interface.
    """

    @property
    def label( self ) :

        """ Label ( any ).
        """

        return self._label

    @label.setter
    def label( self, label : any ) :

        self._label = label

    def __eq__( self, other : any ) -> bool :

        """ Equal.

            Arguments :

                other - Other ( any ).

            Returns :

                equality - Equality ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.label == other.label ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._label = [ ]