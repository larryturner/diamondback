""" **Description**
        Valid interface.

    **Example**
   
        ::
        
            from diamondback import IValid

            class Test( IValid ) :

                def __init__( self ) -> None :
                    super( ).__init__( )
                    self.valid = False

            test = Test( )
            test.valid = True

    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, Analytics & AI, 2020-10-22.
"""

class IValid( object ) :

    """ Valid interface.
    """

    @property
    def valid( self ) :

        """ valid : bool.
        """

        return self._valid

    @valid.setter
    def valid( self, valid : bool ) :

        self._valid = valid

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )
        self._valid = False
