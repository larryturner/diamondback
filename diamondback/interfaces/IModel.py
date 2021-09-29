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
        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, Analytics & AI, 2018-07-12.
"""

from typing import Any

class IModel( object ) :

    """ Model interface.
    """

    @property
    def model( self ) :

        """ model : Any.
        """

        return self._model

    @model.setter
    def model( self, model : Any ) :

        self._model = model

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )
        self._model = None
