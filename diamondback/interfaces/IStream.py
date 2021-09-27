""" **Description**
        Stream interface.

    **Example**
        ::
            from diamondback import IStream
            import sys

            class Test( IStream ) :

                def __init__( self ) -> None :
                    super( ).__init__( )
                    self.stream = sys.stdout

            test = Test( )
            test.stream = sys.stderr

    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, Analytics & AI, 2020-10-15.
"""

from typing import Any

class IStream( object ) :

    """ Stream interface.
    """

    @property
    def stream( self ) :

        """ stream : Any.
        """

        return self._stream

    @stream.setter
    def stream( self, stream : Any ) :

        self._stream = stream

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )
        self._stream = None
