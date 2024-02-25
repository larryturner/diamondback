""" **Description**
        Test ``diamondback`` ``commons``.

    **Example**

        ::

            pytest --capture=no --verbose

    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2024 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, AI Hub, 2018-04-03.
"""

from diamondback import IirFilter
from diamondback import Log, RestClient, Serial
import io
import numpy
import pytest
import sys

class Test( object ) :

    """ Test.
    """

    def test_Log( self ) :

        """ Test Log.
        """

        x = [ str( x ) for x in numpy.random.rand( 3 ) ]
        fio = io.StringIO( )
        Log.stream( fio )
        Log.level( 'Critical' )
        Log.write( 'Debug', f'{numpy.random.rand( 3 ) + 1.0}' )
        Log.level( 'Debug' )
        Log.write( 'Info', x[ 0 ] )
        Log.level( 'Error' )
        Log.write( 'Warning', f'{numpy.random.rand( 3 ) + 1.0}' )
        Log.write( 'Critical', x[ 1 ] )
        Log.write( 'Error', x[ 2 ] )
        value = fio.getvalue( )
        Log.stream( sys.stdout )
        Log.level( 'Info' )
        assert value
        assert value.find( x[ 0 ] ) > 0
        assert value.find( x[ 1 ] ) > value.find( x[ 0 ] )
        assert value.find( x[ 2 ] ) > value.find( x[ 1 ] )

    def test_RestClient( self ) :

        """ Test RestClient.
        """

        client = RestClient( )
        client.url = 'http://en.wikipedia.org'
        assert client.live
        assert client.request( method = 'get', api = '/wiki/Marines' ).content

    def test_Serial( self ) :

        """ Test Serial.
        """

        x = IirFilter( style = 'Butterworth', frequency = 0.1, order = 4, count = 1 )
        for ii in range( 0, 2 ) :
            y = Serial.decode( Serial.encode( x, ii != 0 ), ii != 0 )
            assert ( ( numpy.allclose( x.a, y.a ) ) and ( numpy.allclose( x.b, y.b ) ) and ( numpy.allclose( x.s, y.s ) ) )
            assert Serial.code( Serial.encode( x, compress = False ) ) == Serial.code( Serial.encode( y, compress = False ) )
            with pytest.raises( ValueError ) :
                Serial.decode( Serial.encode( x, bool( ii ) ), not ii )
        x = dict( x = numpy.random.rand( 30, 50 ), y = numpy.random.rand( 50, 30 ) )
        for ii in range( 0, 2 ) :
            y = Serial.decode( Serial.encode( x, ii != 0 ), ii != 0 )
            assert Serial.encode( x, compress = False ) == Serial.encode( y, compress = False )
            assert all( [ u in x for u in list( y.keys( ) ) ] )
        x = '\"\"\" Docstring. \"\"\"\n \
                    { "serial" : { "datetime" : "2019-09-01T15:10:00Z", # Comment.\n \
                                   "duration" : 28800.0,\n \
                                   "period" : 123.4 } }\n'
        y = Serial.decode( x, compress = False, clean = True )
        assert 'serial' in y
        assert all( [ u in y[ 'serial' ] for u in ( 'datetime', 'duration', 'period' ) ] )
        assert numpy.isclose( y[ 'serial' ][ 'period' ], 123.4 )
