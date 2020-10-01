""" **Description**

        Test commons.

    **Example**

        ::

            py.test --capture=no --verbose

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-04-03.

    **Definition**

"""

from diamondback.commons.Log import Log
from diamondback.commons.Serial import Serial
from diamondback.filters.IirFilter import IirFilter
import numpy
import os


def test_Log( count = 2, path = 'test_Log.3.14159.txt' ) :

    """ Test Log.
    """

    try :

        start, error, end = 'Log Test - Start', 'Log Test - Error', 'Log Test - End'

        with open( path, 'w' ) as fout :

            Log.stream( fout )

            Log.level( 'Error' )

            Log.write( 'Debug', error )

            Log.level( 'Debug' )

            Log.write( 'Debug', start )

            Log.write( 'Info', 'X = ', numpy.random.rand( count, count ) )

            Log.write( 'Warning', 'Y = ', list( numpy.random.rand( count, count ) ) )

            Log.write( 'Critical', 'Z = ', set( numpy.random.rand( count ) ) )

            Log.write( 'Error', ValueError( end ) )

        with open( path, 'r' ) as fin :

            x = fin.read( )

            assert x

            assert x.find( start ) >= 0

            assert x.find( error ) < 0

            assert x.find( end ) >= 0

            assert ( ( x.find( 'Critical' ) >= 0 ) and ( x.find( 'Error' ) >= 0 ) and ( x.find( 'Warning' ) >= 0 ) and ( x.find( 'Info' ) >= 0 ) and ( x.find( 'Debug' ) >= 0 ) )

    except Exception as ex :

        assert False

    finally :

        os.remove( path )


def test_Serial( count = 2 ) :

    """ Test Serial.
    """

    obj = IirFilter.Factory.instance( IirFilter, 'Butterworth', 0.1, 4, 1 )

    index = Serial.decode( Serial.encode( obj, False ), False )

    assert obj == index

    index = Serial.decode( Serial.encode( obj, True ), True )

    assert obj == index

    x = { 'array' : numpy.random.rand( count ),
          'list' : list( numpy.random.rand( count ) ),
          'set' : set( numpy.random.rand( count ) ),
          'tuple' : ( list( numpy.random.rand( count ) ) ) }

    y = Serial.decode( Serial.encode( x, False ), False )

    assert ( numpy.allclose( x[ 'array' ], y[ 'array' ] ) )

    assert ( numpy.allclose( x[ 'list' ], y[ 'list' ] ) )

    assert ( numpy.allclose( sorted( x[ 'set' ] ), sorted( y[ 'set' ] ) ) )

    assert ( numpy.allclose( x[ 'tuple' ], y[ 'tuple' ] ) )

    y = Serial.decode( Serial.encode( x, True ), True )

    assert ( numpy.allclose( x[ 'array' ], y[ 'array' ] ) )

    assert ( numpy.allclose( x[ 'list' ], y[ 'list' ] ) )

    assert ( numpy.allclose( sorted( x[ 'set' ] ), sorted( y[ 'set' ] ) ) )

    assert ( numpy.allclose( x[ 'tuple' ], y[ 'tuple' ] ) )

    x = '{ "service" : { "clear" : false, \
                         "datetime" : "2019-09-01T15:10:00Z", \
                         "duration" : 28800.0, \
                         "emulate" : true, \
                         "interval" : 3600.0, \
                         "latency" : 0.0, \
                         "level" : "info", \
                         "name" : { "one" : 1.0, "two" : 2.0, "three" : 3.14159 }, \
                         "optimalstart" : true, \
                         "optimalstop" : true, \
                         "period" : 600.0, \
                         "persistence" : 14400.0, \
                         "write" : false, \
                         "comment" : "JSON instance." } }'

    u = Serial.decode( x, False )

    assert u

    v = Serial.decode( Serial.encode( u, False ), False )

    assert len( u ) == len( v )

    key = list( u.keys( ) )[ 0 ]

    assert ( ( key in u ) and ( key in v ) )

    assert u[ key ] == v[ key ]
