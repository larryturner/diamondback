""" **Description**

        Compress interface.

    **Example**

        ::

            from diamondback import ICompress


            class Test( ICompress ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.compress = False

            test = Test( )

            test.compress = True

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2020, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-10-22.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual


class ICompress( IEqual ) :

    """ Compress interface.
    """

    @property
    def compress( self ) :

        """ Compress ( any ).
        """

        return self._compress

    @compress.setter
    def compress( self, compress : any ) :

        self._compress = compress

    def __eq__( self, other : any ) -> bool :

        """ Equality.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.compress == other.compress ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._compress = [ ]
