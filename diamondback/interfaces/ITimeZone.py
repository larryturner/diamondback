""" **Description**

        Time zone interface.

    **Example**

        ::

            from diamondback.interfaces.ITimeZone import ITimeZone
            import datetime


            class Test( ITimeZone ) :

                def __init__( self ) :

                    super( ).__init__( )

                    self.timezone = datetime.timezone.utc

            test = Test( )

            test.timezone = datetime.datetime.now( ).astimezone( ).tzinfo

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-07-12.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import datetime


class ITimeZone( IEqual ) :

    """ Time zone interface.
    """

    @property
    def timezone( self ) :

        """ Time zone ( datetime.timezone ).
        """

        return self._timezone

    @timezone.setter
    def timezone( self, timezone ) :

        if ( not timezone ) :

            raise ValueError( 'TimeZone = ' + str( timezone ) )

        self._timezone = timezone

    def __eq__( self, other ) :

        """ Evaluates equality condition.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.timezone == other.timezone ) )

    def __init__( self ) :

        """ Initializes an instance.
        """

        super( ).__init__( )

        self._timezone = datetime.timezone.utc
