""" **Description**

        Data interface.

    **Example**

        ::

            from diamondback.interfaces.IData import IData


            class Test( IData ) :

                def __init__( self ) :

                    super( ).__init__( )

                    self.data = [ ]

            test = Test( )

            test.data = { 'a' : 0.0, 'b' : 1.0 }

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-07-12.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual


class IData( IEqual ) :

    """ Data interface.
    """

    @property
    def data( self ) :

        """ Data ( array( object ), list( object ), set( object ), tuple( object ), dict( object, object ) ).
        """

        return self._data

    @data.setter
    def data( self, data ) :

        self._data = data

    def __eq__( self, other ) :

        """ Evaluates equality condition.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.data == other.data ) )

    def __init__( self ) :

        """ Initializes an instance.
        """

        super( ).__init__( )

        self._data = [ ]
