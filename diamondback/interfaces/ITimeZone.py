"""" **Description**

        Time zone interface.

    **Example**

        ::

            from diamondback import ITimeZone
            import datetime
            import pytz


            class Test( ITimeZone ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.timezone = datetime.timezone.utc

            test = Test( )

            test.timezone = pytz.timezone( 'US/Eastern' )

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

        """ Time zone ( timezone ).
        """

        return self._timezone

    @timezone.setter
    def timezone( self, timezone : datetime.timezone ) :

        if ( not timezone ) :

            raise ValueError( 'TimeZone = ' + str( timezone ) )

        self._timezone = timezone

    def __eq__( self, other : any ) -> bool :

        """ Equality.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.timezone == other.timezone ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._timezone = datetime.timezone.utc
