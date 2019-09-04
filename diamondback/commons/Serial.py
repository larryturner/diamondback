""" **Description**

        A serial instance encodes and decodes an instance or collection with
        JSON text, or base-64 encoded gzip JSON binary format.

        An instance may be an object or a collection, referenced by abstract or
        concrete types, and the instance will be correctly encoded and decoded.
        JSON binary format is selected by electing to compress.  Encoding may
        be specified if an alternative to UTF-8 is required.  Comments may be
        filtered from JSON text by electing to clean.

        Singleton.

    **Example**

        ::

            from diamondback.commons.Serial import Serial

            x = { 'a' : numpy.random.rand( count ),
                  'b' : list( numpy.random.rand( count ) ) }

            z = Serial.decode( Serial.encode( x, False ), False )

            y = Serial.encode( x, True )

            z = Serial.decode( y, True )

            z = Serial.decode( '{ "a" : 1.0, "b" : 2.0, "c" : 3.14159 }', False )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-07-13.

    **Definition**

"""

import base64
import gzip
import jsonpickle
import jsonpickle.ext.numpy
import re


class Serial( object ) :

    """ Serial service, with JSON text or base-64 encoded gzip JSON binary format.
    """

    jsonpickle.ext.numpy.register_handlers( )

    @staticmethod
    def decode( state, compress = True, encoding = 'utf_8', clean = False ) :

        """ Decodes an instance.

            Arguments :

                state - State ( str ).

                compress - Compress ( bool ).

                encoding - Encoding ( str ).

                clean - Clean comments ( bool ).

            Returns :

                instance - Instance ( object, array( object ), list( object ), set( object ), tuple( object ), dict( object, object ) ).
        """

        if ( not state ) :

            raise ValueError( 'state = ' + str( state ) )

        if ( not encoding ) :

            raise ValueError( 'encoding = ' + str( encoding ) )

        if ( compress ) :

            state = str( gzip.decompress( base64.b64decode( bytes( state, encoding ) ) ), encoding )

        if ( clean ) :

            state = re.sub( re.compile( '#.*?\n', re.DOTALL ), '', re.sub( re.compile( '\""".*?\"""', re.DOTALL ), '', state ) )

        return jsonpickle.decode( state )

    @staticmethod
    def encode( instance, compress = True, encoding = 'utf_8' ) :

        """ Encodes an instance.

            Arguments :

                instance - Instance ( object, array( object ), list( object ), set( object ), tuple( object ), dict( object, object ) ).

                compress - Compress ( bool ).

                encoding - Encoding ( str ).

            Returns :

                state - State ( str ).
        """

        if ( not instance ) :

            raise ValueError( 'instance = ' + str( instance ) )

        if ( not encoding ) :

            raise ValueError( 'encoding = ' + str( encoding ) )

        state = jsonpickle.encode( instance )

        if ( compress ) :

            state = str( base64.b64encode( gzip.compress( bytes( state, encoding ) ) ), encoding )

        return state
