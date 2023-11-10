""" **Description**
        A serial instance encodes and decodes an instance or collection in
        BSON or JSON, and generates SHA3-256 codes, using the jsonpickle
        package.

        BSON, Base-85 encoded gzip JSON, embeds a datetime context, and code
        will not be consistent or useful for validation.

        An instance may be an object or a collection, referenced by abstract or
        concrete types, and the instance will be correctly encoded and decoded,
        without custom encoding definitions.  BSON binary format is selected by
        electing to compress.  Encoding may be specified if an alternative to
        UTF-8 is required.

        Comments may be filtered from JSON by electing to clean.  Python style
        docstring and line comments are supported, though line comments must be
        terminated by a new line.

        Singleton.

        Thread safe.

    **Example**

        ::

            from diamondback import Serial
            import numpy
            import pandas

            # Encode and decode a dictionary in JSON.

            n = numpy.random.randint( 1, 10 )
            x = dict( a = numpy.random.rand( n ), b = list( numpy.random.rand( n ) ) )
            y = Serial.encode( x, indent = True )
            z = Serial.decode( y )

            # Encode and decode a dictionary in BSON.

            y = Serial.encode( x, compress = True )
            z = Serial.decode( y, compress = True )

            # Encode and decode a pandas DataFrame in BSON.

            model = pandas.DataFrame( dict( fruit = [ 'orange', 'apple', 'kiwi' ], value = [ 1.25, 1.5, 0.30 ] ) )
            y = Serial.encode( model )

            # Generate an SHA3-256 code.

            code = Serial.code( y )
            z = Serial.decode( y )

            # Decode in JSON.

            z = Serial.decode( '{ "a" : 1.0, "b" : 2.0, "c" : 3.14159 }' )
            z = Serial.decode( '[ 1.0, 2.0, 3.0 ]' )

    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2023 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, AI Hub, 2018-07-13.
"""

from typing import Any
import base64
import gzip
import hashlib
import jsonpickle
import jsonpickle.ext.numpy
import jsonpickle.ext.pandas
import re

class Serial( object ) :

    """ Serial.
    """

    jsonpickle.ext.numpy.register_handlers( )
    jsonpickle.ext.pandas.register_handlers( )

    @staticmethod
    def code( state : str, encoding : str = 'utf_8' ) -> str :

        """ Code generation.  SHA3-256 hash.

            Arguments :
                state : str.
                encoding : str.

            Returns :
                code : str.
        """

        if ( not state ) :
            raise ValueError( f'State = {state}' )
        if ( not encoding ) :
            raise ValueError( f'Encoding = {encoding}' )
        return hashlib.sha3_256( bytes( state, encoding ) ).hexdigest( )

    @staticmethod
    def decode( state : str, compress : bool = False, encoding : str = 'utf_8', clean : bool = False ) -> Any :

        """ Decodes an instance or collection from a BSON or JSON state.
            Encoding may be specified if an alternative to UTF-8 is required.
            Python style docstring and line comments may be cleaned, though
            line comments must be terminated by a new line.

            Arguments :
                state : str.
                compress : bool.
                encoding : str.
                clean : bool - clean comments.

            Returns :
                instance : Any.
        """

        if ( not state ) :
            raise ValueError( f'State = {state}' )
        if ( not encoding ) :
            raise ValueError( f'Encoding = {encoding}' )
        if ( compress ) :
            state = str( gzip.decompress( base64.b85decode( bytes( state, encoding ) ) ), encoding )
        if ( clean ) :
            state = re.sub( re.compile( '#.*?\n', re.DOTALL ), '', re.sub( re.compile( '\""".*?\"""', re.DOTALL ), '', state ) )
        return jsonpickle.decode( state )

    @staticmethod
    def encode( instance : Any, compress : bool = False, encoding : str = 'utf_8', indent : bool = False ) -> str :

        """ Encodes BSON or JSON.  Encoding may be specified if an alternative
            to UTF-8 is required.

            Arguments :
                instance : Any.
                compress : bool.
                encoding : str.
                indent : bool.

            Returns :
                state : str.
        """

        if ( not encoding ) :
            raise ValueError( f'Encoding = {encoding}' )
        state = jsonpickle.encode( instance, indent = '    ' if ( indent ) else None, separators = ( ',', ':' ) )
        if ( compress ) :
            state = str( base64.b85encode( gzip.compress( bytes( state, encoding ) ) ), encoding )
        return state
