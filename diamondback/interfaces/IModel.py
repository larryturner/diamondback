""" **Description**

        Model interface.

    **Example**

        ::

            from diamondback import IModel, Serial

            class Test( IModel ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.model = [ ]

            test = Test( )

            test.model = Serial.encode( { 'a' : 0.0, 'b' : 1.0 } )

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-07-12.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual


class IModel( IEqual ) :

    """ Model interface.
    """

    @property
    def model( self ) :

        """ model : any.
        """

        return self._model

    @model.setter
    def model( self, model : any ) :

        self._model = model

    def __eq__( self, other : any ) -> bool :

        """ Equal.

            Arguments :

                other : any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( self.model == other.model ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._model = None
