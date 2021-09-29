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
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, Analytics & AI, 2018-07-12.
"""

import datetime

class ITimeZone( object ) :

    """ Time zone interface.
    """

    @property
    def timezone( self ) :

        """ timezone : datetime.timezone.
        """

        return self._timezone

    @timezone.setter
    def timezone( self, timezone : datetime.timezone ) :

        if ( not timezone ) :
            raise ValueError( f'TimeZone = {timezone}' )
        self._timezone = timezone

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )
        self._timezone = datetime.timezone.utc
