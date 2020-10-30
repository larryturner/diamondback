""" **Description**

        Cache interface.

    **Example**

        ::

            from diamondback.interfaces.ICache import ICache


            class Test( ICache ) :

                def __init__( self ) -> None :

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

        """ Cache ( any ).
        """

        return self._cache

    @cache.setter
    def cache( self, cache : any ) :

        self._cache = cache

    def __eq__( self, other : any ) -> bool :

        """ Equality.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.cache == other.cache ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._cache = [ ]
