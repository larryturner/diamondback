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

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-11-02.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import getpass


class IUser( IEqual ) :

    """ User interface.
    """

    @property
    def user( self ) :

        """ user : str.
        """

        try :

            value = getpass.getuser( )

        except :

            value = ''

        return value

    def __eq__( self, other : any ) -> bool :

        """ Equal.

            Arguments :

                other : any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( self.user == other.user ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )
