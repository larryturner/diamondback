""" **Description**

        Encoding interface.

    **Example**

        ::

            from diamondback.interfaces.IEncoding import IEncoding


            class Test( IEncoding ) :

                def __init__( self ) :

                    super( ).__init__( )

                    self.encoding = ( )

            test = Test( )

            test.encoding = ( 0.0, 1.0 )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2019, Larry Turner, Schneider Electric.  All rights reserved.

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

        """ Encoding ( object, array( object ), list( object ), set( object ), tuple( object ), dict( object, object ) ).
        """

        return self._encoding

    @encoding.setter
    def encoding( self, encoding ) :

        self._encoding = encoding

    def __eq__( self, other ) :

        """ Evaluates equality condition.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.encoding == other.encoding ) )

    def __init__( self ) :

        """ Initializes an instance.
        """

        super( ).__init__( )

        self._encoding = [ ]
