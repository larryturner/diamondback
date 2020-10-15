""" **Description**

        Cache interface.

    **Example**

        ::

            from diamondback.interfaces.IUrl import ICache


            class Test( ICach ) :

                def __init__( self ) :

                    super( ).__init__( )

                    self.cache = False

            test = Test( )

            test.cache = True

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2020, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2020-10-15.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual


class ICache( IEqual ) :

    """ Cache interface.
    """

    @property
    def cache( self ) :

        """ Cache ( object, array( object ), list( object ), set( object ), tuple( object ), dict( object, object ) ).
        """

        return self._cache

    @cache.setter
    def cache( self, cache ) :

        self._cache = cache

    def __eq__( self, other ) :

        """ Evaluates equality condition.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.cache == other.cache ) )

    def __init__( self ) :

        """ Initializes an instance.
        """

        super( ).__init__( )

        self._cache = [ ]
