""" **Description**

        Write interface.

    **Example**

        ::

            from diamondback import IWrite


            class Test( IWrite ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.write = False

            test = Test( )

            test.write = True

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2020, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-10-15.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual


class IWrite( IEqual ) :

    """ Write interface.
    """

    @property
    def write( self ) :

        """ Write ( any ).
        """

        return self._write

    @write.setter
    def write( self, write : any ) :

        self._write = write

    def __eq__( self, other : any ) -> bool :

        """ Equality.

            Arguments :

                other - Other ( any ).

            Returns :

                equality - Equality ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.write == other.write ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._write = [ ]
