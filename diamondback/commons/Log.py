""" **Description**

        A log instance formats and writes log entries, electively using the
        logger package or directly to a specified stream.  Log entries are
        prefaced with an ISO-8601 datetime and log level, and enhancements are
        made to the formatting of datetime, exception, and collection data
        types.  Dynamic stream redirection and log level specification are
        supported.

        If a stream is defined and associated with a specified name, the
        standard logging package is used in subsequent interactions with a log,
        a logger instance is defined with the specified name, a logging stream
        handler is associated with the stream, and log levels are synchronized
        with logging levels.

        Singleton.

        Thread safe and reentrant.

    **Example**

        ::

            from diamondback.commons.Log import Log
            import io
            import numpy
            import pytz
            import sys


            try :

                # Default - Log stream is sys.stdout, logging package is not used, level is 'Info', and timezone is UTC.

                # Set Log level to 'Info'.

                Log.level( 'Info' )

                # Write an 'Info' entry with UTC timezone.

                Log.write( 'Info', 'Hello' )

                # Write an 'Info' entry with 'US/Eastern' timezone.

                Log.timezone( pytz.timezone( 'US/Eastern' ) )

                Log.write( 'Info', 'World', ( 'Example', 'Data', 'Payload' ) )

                # Set Log stream to sys.stdout, use logging as 'project_log', and write an 'Info' entry.

                Log.stream( sys.stdout, 'project_log' )

                Log.write( 'Info', 'Valid = ', True )

                # Set Log stream to a memory stream, write an Info entry, and read and reset the stream.

                stream = io.StringIO( )

                Log.stream( stream )

                x = numpy.random.rand( 2, 2 )

                Log.write( 'Info', 'X = ', x )

                value = stream.getvalue( )

                _, _ = stream.truncate( 0 ), stream.seek( 0 )

                # Set Log stream to a file and write a 'Warning' entry.

                with open( 'log.000.txt', 'w' ) as fout :

                    Log.stream( fout )

                    x = numpy.random.rand( 2, 2 )

                    Log.write( 'Warning', 'X = ', x )

            except Exception as ex :

                # Write an 'Error' entry on Exception.

                Log.write( ex, 'Error' )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-03-22.

    **Definition**

"""

from threading import RLock
import datetime
import logging
import numpy
import os
import sys
import typing


class Log( object ) :

    """ Log service.
    """

    numpy.set_printoptions( formatter = { 'float' : '{: .6f}'.format } )

    _handler = [ ]

    _level, _log = 'Info', [ ]

    _map = { 'Critical' : logging.CRITICAL,
             'Error' : logging.ERROR,
             'Warning' : logging.WARNING,
             'Info' : logging.INFO,
             'Debug' : logging.DEBUG }

    _rlock = RLock( )

    _stream, _timezone = sys.stdout, datetime.timezone.utc

    @classmethod
    def level( cls, level : str ) -> None :

        """ Level.

            Arguments :

                level - Level in ( 'Critical', 'Error', 'Warning', 'Info', 'Debug' ) ( str ).
        """

        with ( Log._rlock ) :

            if ( not level ) :

                raise ValueError( 'Level = ' + str( level ) )

            level = level.title( )

            if ( level != Log._level ) :

                if ( level not in Log._map ) :

                    raise ValueError( 'Level = ' + str( level ) )

                if ( Log._log ) :

                    Log._log.setLevel( Log._map[ level ] )

                Log._level = level

    @classmethod
    def stream( cls, stream : any, name : str = None ) -> None :

        """ Stream.

            Arguments :

                stream - Stream ( sys.stderr, sys.stdout, open( < path >, 'w' or 'a' ) ).

                name - Logger name if not empty ( str ).
        """

        with ( Log._rlock ) :

            if ( not stream ) :

                raise ValueError( 'Stream = ' + str( stream ) )

            if ( Log._log ) :

                Log._log.removeHandler( Log._handler )

                Log._handler, Log._log = [ ], [ ]

            if ( name ) :

                Log._handler = logging.StreamHandler( stream )

                Log._log = logging.getLogger( name )

                Log._log.addHandler( Log._handler )

                Log._log.setLevel( Log._map[ Log._level ] )

            Log._stream = stream

    @classmethod
    def timezone( cls, timezone : datetime.timezone ) -> None :

        """ Timezone.

            Arguments :

                timezone - Time zone ( timezone ).
        """

        with ( Log._rlock ) :

            if ( not timezone ) :

                raise ValueError( 'TimeZone = ' + str( timezone ) )

            Log._timezone = timezone

    @classmethod
    def write( cls, level : str, entry : typing.Union[ Exception, str ], data : any = None ) -> None :

        """ Formats and writes log entries, electively using the logger package
            or directly to a specified stream.  Log entries are prefaced with
            an ISO-8601 datetime and log level, and enhancements are made to
            the formatting of datetime, exception, and collection data types.

            Arguments :

                level - Level in ( 'Critical', 'Error', 'Warning', 'Info', 'Debug' ) ( str ).

                entry - Entry ( Exception, str ).

                data - Data ( any ).
        """

        with ( Log._rlock ) :

            level = level.title( )

            if ( Log._map[ level ] >= Log._map[ Log._level ] ) :

                try :

                    s = '{:30s}{:10s}'.format( datetime.datetime.utcnow( ).replace( microsecond = 0, tzinfo = datetime.timezone.utc ).astimezone( Log._timezone ).isoformat( ), level )

                    if ( isinstance( entry, Exception ) ) :

                        s += '{:30s}{:s}'.format( type( entry ).__name__, str( entry ) )

                        info = sys.exc_info( )[ -1 ]

                        while ( info ) :

                            s += os.linesep + '{:40s}@ {:s} {:s} {:d}'.format( '', info.tb_frame.f_code.co_filename.split( os.sep )[ -1 ],
                                                                                   info.tb_frame.f_code.co_name,
                                                                                   info.tb_lineno )

                            info = info.tb_next

                    else :

                        s += str( entry )

                    try :

                        if ( data is not None ) :

                            if ( len( data ) > 0 ) :

                                if ( isinstance( data, str ) ) :

                                    s += ' ' + str( data )

                                else :

                                    s += ' ' + str( data ).replace( '(', '( ' ).replace( ')', ' )' ).replace( '[', '[ ' ).replace( ']', ' ]' ).replace( '{', '{ ' ).replace( '}', ' }' )

                    except :

                        s += ' ' + str( data )

                    if ( Log._log ) :

                        Log._log.log( Log._map[ level ], s )

                    else :

                        _ = Log._stream.write( s + os.linesep )

                except :

                    pass
