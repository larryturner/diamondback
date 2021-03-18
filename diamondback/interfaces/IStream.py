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

        Copyright (c) 2020, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-10-15.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual


class IStream( IEqual ) :

    """ Stream interface.
    """

    @property
    def stream( self ) :

        """ Stream ( any ).
        """

        return self._stream

    @stream.setter
    def stream( self, stream : any ) :

        self._stream = stream

    def __eq__( self, other : any ) -> bool :

        """ Equal.

            Arguments :

                other - Other ( any ).

            Returns :

                equality - Equality ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.stream == other.stream ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._stream = [ ]
