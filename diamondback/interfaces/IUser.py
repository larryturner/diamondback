""" **Description**

        User interface.

    **Example**

        ::

            from diamondback import IUser


            class Test( IUser ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

            test = Test( )

            print( test.user )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2020, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-11-02.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import os


class IUser( IEqual ) :

    """ User interface.
    """

    @property
    def user( self ) :

        """ User ( str ).
        """

        try :

            value = os.getlogin( )

        except :

            value = ''

        return value

    def __eq__( self, other : any ) -> bool :

        """ Equality.

            Arguments :

                other - Other ( any ).

            Returns :

                equality - Equality ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.user == other.user ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )
