""" **Description**

        A log instance formats and writes log entries with a specified level
        and stream using the loguru package. Log entries contain an ISO-8601
        datetime and level.  Dynamic stream redirection and level specification
        are supported.

        Log uses lazy initialization to coexist with loguru, and removes or
        creates loguru handlers only on explicit stream assignment or write.
        In lazy initialization an existing default loguru handler, with an
        identity equal to 0, and a stream assignment of sys.stdout is removed,
        and a new loguru handler with a stream assignment of sys.stdout and a
        level of 'INFO' is created.

        In stream assignments subsequent to initialization, only loguru
        handlers previously created by Log will be removed, as the design
        pattern does not support multicast.  The ability to create and modify
        externally defined loguru handlers, multicast, and utilize any native
        loguru functionality is supported.

        Levels defined by loguru are supported, including custom definitions.
        The level may be dynamically modified without creating, deleting, or
        modifying a loguru handler.

        Singleton.

        Thread safe.

    **Example**

        ::

            from diamondback import Log
            import io
            import numpy
            import sys


            try :

                # Set Log level to 'INFO', the default level.

                Log.level( 'INFO' )

                Log.write( 'INFO', 'Test Log write.' )

                # Set Log stream to sys.stdout.

                Log.stream( sys.stdout )

                Log.write( 'INFO', f'Valid = {True}' )

                # Set Log stream to a memory stream.

                stream = io.StringIO( )

                Log.stream( stream )

                x = numpy.random.rand( 2, 2 )

                Log.write( 'INFO', f'X = {x}' )

                # Read and reset memory stream.

                value = stream.getvalue( )

                _, _ = stream.truncate( 0 ), stream.seek( 0 )

                # Set Log stream to a file.

                with open( 'log.000.txt', 'w' ) as fout :

                    Log.stream( fout )

                    x = numpy.random.rand( 2, 2 )

                    Log.write( 'WARNING', f'X = {x}' )

            except Exception as ex :

                Log.write( 'ERROR', ex )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-03-22.

    **Definition**

"""

from loguru import logger
from threading import RLock
import numpy
import os
import sys


class Log( object ) :

    """ Log service.
    """

    numpy.set_printoptions( formatter = { 'float' : '{:.6f}'.format } )

    _identity, _level = 0, logger.level( 'INFO' )

    _rlock = RLock( )

    @classmethod
    def level( cls, level : str ) -> None :

        """ Level.

            Arguments :

                level : str - in ( 'CRITICAL', 'ERROR', 'WARNING', 'SUCCESS', 'INFO', 'DEBUG', 'TRACE', ... < custom > ).
        """

        with ( Log._rlock ) :

            try :

                Log._level = logger.level( level.upper( ) )

            except :

                raise ValueError( f'Level = {level}' )

    @classmethod
    def stream( cls, stream : any ) -> None :

        """ Stream.

            Arguments :

                stream : ( sys.stderr, sys.stdout, open( < path >, 'w' or 'a' ) ).
        """

        with ( Log._rlock ) :

            if ( ( not stream ) or ( not hasattr( stream, 'write' ) ) ) :

                raise ValueError( f'Stream = {stream}' )

            try :

                logger.remove( Log._identity )

            except :

                pass

            Log._identity = logger.add( stream, level = 10, format = '<blue>{time:YYYY-MM-DDTHH:mm:ss.SSZ}</blue> <level>{level}</level> {message}' )

    @classmethod
    def write( cls, level : str, entry : any ) -> None :

        """ Formats and writes log entries using the loguru package with a
            specified level and stream.  Log entries contain an ISO-8601
            datetime and level.

            Arguments :

                level : str - in ( 'CRITICAL', 'ERROR', 'WARNING', 'SUCCESS', 'INFO', 'DEBUG', 'TRACE', ... < custom > ).

                entry : any.
        """

        with ( Log._rlock ) :

            try :

                if ( not Log._identity ) :

                    Log.stream( sys.stdout )

                level = logger.level( level.upper( ) )

            except :

                raise ValueError( f'Level = {level}' )

            if ( level.no >= Log._level.no ) :

                try :

                    if ( isinstance( entry, Exception ) ) :

                        entry = f'Exception = {type( entry ).__name__} {entry}'

                        info = sys.exc_info( )[ -1 ]

                        while ( info ) :

                            entry += f' @ File = {info.tb_frame.f_code.co_filename.split( os.sep )[ -1 ]} Line = {info.tb_lineno}'

                            info = info.tb_next

                    logger.log( level.name, entry )

                except :

                    pass
