""" **Description**

        Encoding interface.

    **Example**

        ::

            from diamondback import IEncoding


            class Test( IEncoding ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.encoding = 'utf-8'

            test = Test( )

            test.encoding = 'utf-16'

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

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

        """ encoding : any.
        """

        return self._encoding

    @encoding.setter
    def encoding( self, encoding : any ) :

        self._encoding = encoding

    def __eq__( self, other : any ) -> bool :

        """ Equal.

            Arguments :

                other : any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( self.encoding == other.encoding ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._encoding = None
