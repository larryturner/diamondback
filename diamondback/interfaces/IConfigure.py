""" **Description**
        Configure interface.

    **Example**
        ::
            from diamondback import IConfigure

            class Test( IConfigure ) :

                def __init__( self ) -> None :
                    super( ).__init__( )
                    self.configure = [ ]

            test = Test( )
            test.configure = { 'a' : 0.0, 'b' : 1.0 }

    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, Analytics & AI, 2020-10-27.
"""

from typing import Any

class IConfigure( object ) :

    """ Configure interface.
    """

    @property
    def configure( self ) :

        """ configure : Any.
        """

        return self._configure

    @configure.setter
    def configure( self, configure : Any ) :

        self._configure = configure

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )
        self._configure = None
