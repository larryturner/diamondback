""" **Description**

        A log instance formats and writes log entries, electively using the
        logger package or directly to a specified stream.  Log entries are
        prefaced with an ISO-8601 UTC datetime and log level, and enhancements
        are made to the formatting of datetime, exception, and collection data
        types.  Dynamic stream redirection and log level specification are
        supported.

        If a stream is defined and associated with a specified name, the
        standard logging package is used in subsequent interactions with a log,
        a logger instance is defined with the specified name, a logging stream
        handler is associated with the stream, and log levels are synchronized
        with logging levels.

        Singleton.

    **Example**

        ::

            from diamondback.commons.Log import Log
            import numpy
            import sys

            try :

                Log.level( 'Info' )

                with open( 'log.000.txt', 'w' ) as fout :

                    Log.stream( fout )

                    Log.write( 'Warning', 'x = ', numpy.random.rand( 2, 2 ) )

                Log.stream( sys.stdout, 'project_log' )

                Log.write( 'Info', 'y = [ ]' )

            except Exception as ex :

                Log.write( ex, 'Error' )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-03-22.

    **Definition**

"""

import datetime
import logging
import numpy
import os
import sys
import traceback


class Log( object ) :

    """ Log service.
    """

    numpy.set_printoptions( formatter = { 'float' : '{: .6f}'.format } )

    _handler = [ ]

    _level = 'Info'

    _log = [ ]

    _map = { 'Critical' : logging.CRITICAL,
             'Error' : logging.ERROR,
             'Warning' : logging.WARNING,
             'Info' : logging.INFO,
             'Debug' : logging.DEBUG }

    _stream = sys.stdout

    @classmethod
    def level( cls, level ) :

        """ Level.

            Arguments :

                level - Level in ( 'Critical', 'Error', 'Warning', 'Info', 'Debug' ) ( str ).
        """

        level = level.title( )

        if ( level != Log._level ) :

            if ( level not in Log._map ) :

                raise ValueError( 'level = ' + str( level ) )

            if ( Log._log ) :

                Log._log.setLevel( Log._map[ level ] )

            Log._level = level

    @classmethod
    def stream( cls, stream, name = '' ) :

        """ Stream.

            Arguments :

                stream - Stream ( sys.stderr, sys.stdout, open( < path >, 'w' or 'a' ) ).

                name - Logger name if not empty ( str ).
        """

        if ( not stream ) :

            raise ValueError( 'stream = ' + str( stream ) )

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
    def write( cls, level, entry, data = None ) :

        """ Writes log entry.

            Arguments :

                level - Level in ( 'Critical', 'Error', 'Warning', 'Info', 'Debug' ) ( str ).

                entry - Entry ( Exception, str ).

                data - Data ( object, array( object ), list( object ), set( object ), tuple( object ), dict( object, object ) ).
        """

        level = level.title( )

        if ( Log._map[ level ] >= Log._map[ Log._level ] ) :

            try :

                s = '{:30s}{:10s}'.format( datetime.datetime.utcnow( ).replace( microsecond = 0, tzinfo = datetime.timezone.utc ).isoformat( )[ : 19 ], level )

                if ( isinstance( entry, Exception ) ) :

                    s += str( entry.__class__ ).replace( '<class ', '' ).replace( '>', '' ) + ' ' + str( entry ) + os.linesep

                    trace = traceback.format_exception( None, entry, entry.__traceback__ )

                    for ii in range( 1, len( trace ) - 1 ) :

                        s += trace[ ii ].replace( 'File', '@' ).replace( 'line ', '' ).replace( '"', '' )

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
