""" **Description**

        Header interface.

    **Example**

        ::

            from diamondback import IHeader


            class Test( IHeader ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.header = { }


            test = Test( )

            test.header = { 'content-encoding' : 'gzip', 'content-type' : 'application/json' }

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2020, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-09-25.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import typing


class IHeader( IEqual ) :

    """ Header interface.
    """

    @property
    def header( self ) :

        """ header : str.
        """

        return self._header

    @header.setter
    def header( self, header : typing.Dict[ str, str ] ) :

        self._header = header

    def __eq__( self, other : any ) -> bool :

        """ Equal.

            Arguments :

                other : any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( self.header == other.header ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._header = { }
