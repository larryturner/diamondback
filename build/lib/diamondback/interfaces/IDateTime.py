"""" **Description**

        Date time interface.

    **Example**

        ::

            from diamondback.interfaces.IDateTime import IDateTime
            import datetime


            class Test( IDateTime ) :

                def __init__( self ) :

                    super( ).__init__( )

                    self.datetime = datetime.datetime.utcnow( )

            test = Test( )

            test.datetime += datetime.timedelta( hours = 4 )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-07-12.

    **Definition**

"""

from diamondback.interfaces.ITimeZone import ITimeZone
import datetime


class IDateTime( ITimeZone ) :

    """ Date time interface.
    """

    @property
    def datetime( self ) :

        """ Date time ( datetime ).
        """

        return self._datetime

    @datetime.setter
    def datetime( self, datetim ) :

        if ( not datetim ) :

            raise ValueError( 'DateTime = ' + str( datetim ) )

        self._datetime = datetim.replace( microsecond = 0 ).astimezone( self.timezone )

    @ITimeZone.timezone.setter
    def timezone( self, timezone ) :

        """ Time zone ( datetime.timezone ).
        """

        ITimeZone.timezone.fset( self, timezone )

        self.datetime = self.datetime

    def __eq__( self, other ) :

        """ Evaluates equality condition.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.datetime == other.datetime ) )

    def __init__( self ) :

        """ Initializes an instance.
        """

        super( ).__init__( )

        self._datetime = datetime.datetime.utcnow( ).replace( microsecond = 0, tzinfo = datetime.timezone.utc ).astimezone( self.timezone )
