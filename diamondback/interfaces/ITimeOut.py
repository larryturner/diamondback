""" **Description**
        Time out interface.

    **Example**
     
        ::
        
            from diamondback import ITimeOut

            class Test( ITimeOut ) :

                def __init__( self ) -> None :
                    super( ).__init__( )
                    self.timeout = ( 10.0, 60.0 )

            test = Test( )
            test.timeout = ( 15.0, 120.0 )

    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, Analytics & AI, 2019-10-09.
"""

from typing import Any

class ITimeOut( object ) :

    """ Time out interface.
    """

    @property
    def timeout( self ) :

        """ timeout : Any.
        """

        return self._timeout

    @timeout.setter
    def timeout( self, timeout : Any ) :

        self._timeout = timeout

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )
        self._timeout = None
