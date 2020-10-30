""" **Description**

        Encoding interface.

    **Example**

        ::

            from diamondback.interfaces.IEncoding import IEncoding


            class Test( IEncoding ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.encoding = ( )

            test = Test( )

            test.encoding = ( 0.0, 1.0 )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2019, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2019-10-09.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual


class IEncoding( IEqual ) :

    """ Encoding interface.
    """

    @property
    def encoding( self ) :

        """ Encoding ( any ).
        """

        return self._encoding

    @encoding.setter
    def encoding( self, encoding : any ) :

        self._encoding = encoding

    def __eq__( self, other : any ) -> bool :

        """ Equality.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.encoding == other.encoding ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._encoding = [ ]
