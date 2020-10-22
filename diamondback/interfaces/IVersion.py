""" **Description**

        Version interface.

    **Example**

        ::

            from diamondback.interfaces.IVersion import IVersion


            class Test( IVersion ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.version = '1.0.0'

            test = Test( )

            test.version = '1.0.1'

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2020, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-09-23.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual


class IVersion( IEqual ) :

    """ Version interface.
    """

    @property
    def version( self ) :

        """ Version ( any ).
        """

        return self._version

    @version.setter
    def version( self, version : any ) :

        self._version = version

    def __eq__( self, other : any ) -> bool :

        """ Evaluates equality condition.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.version == other.version ) )

    def __init__( self ) -> None :

        """ Initializes an instance.
        """

        super( ).__init__( )

        self._version = [ ]
