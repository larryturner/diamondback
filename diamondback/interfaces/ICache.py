""" **Description**

        Cache interface.

    **Example**

        ::

            from diamondback import ICache


            class Test( ICache ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.cache = False

            test = Test( )

            test.cache = True

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

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

        """ cache : any.
        """

        return self._cache

    @cache.setter
    def cache( self, cache : any ) :

        self._cache = cache

    def __eq__( self, other : any ) -> bool :

        """ Equal.

            Arguments :

                other : any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( self.cache == other.cache ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._cache = None
