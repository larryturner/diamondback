"""" **Description**

        Date interface.

    **Example**

        ::

            from diamondback import IDate
            import datetime


            class Test( IDate ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.date = datetime.datetime.utcnow( ).replace( microsecond = 0, tzinfo = datetime.timezone.utc )

            test = Test( )

            test.date += datetime.timedelta( hours = 4 )

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-07-12.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import datetime


class IDate( IEqual ) :

    """ Date interface.
    """

    @property
    def date( self ) :

        """ date : datetime.datetime.
        """

        return self._date

    @date.setter
    def date( self, date : datetime.datetime ) :

        if ( not date ) :

            raise ValueError( f'Date = {date}' )

        if ( not date.tzinfo ) :

            date = date.replace( tzinfo = datetime.timezone.utc )

        self._date = date.replace( microsecond = 0 )

    def __eq__( self, other : any ) -> bool :

        """ Equal.

            Arguments :

                other : any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( self.date == other.date ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._date = datetime.datetime.utcnow( ).replace( microsecond = 0, tzinfo = datetime.timezone.utc )
