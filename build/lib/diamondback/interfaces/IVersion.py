""" **Description**

        Version interface.

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

        """ Version ( object, array( object ), list( object ), set( object ), tuple( object ), dict( object, object ) ).
        """

        return self._version

    @version.setter
    def version( self, version ) :

        self._version = version

    def __eq__( self, other ) :

        """ Evaluates equality condition.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.version == other.version ) )

    def __init__( self ) :

        """ Initializes an instance.
        """

        super( ).__init__( )

        self._version = [ ]