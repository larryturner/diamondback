""" **Description**

        A serial instance encodes and decodes an instance or collection with
        JSON or BSON, base-85 encoded gzip JSON, format using the jsonpickle
        package.

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


            # Encode and decode a dictionary instance in JSON.

            x = { 'a' : numpy.random.rand( count ), 'b' : list( numpy.random.rand( count ) ) }

            z = Serial.decode( Serial.encode( x ) )

            # Encode and decode a dictionary instance in BSON.

            y = Serial.encode( x, compress = True )

            z = Serial.decode( y, compress = True )

            # Encode and decode a pandas data frame in BSON.

            model = pandas.DataFrame( { 'fruit' : [ 'orange', 'apple', 'kiwi' ], 'Cost' : [ 1.25, 1.5, 0.30 ] } )

            y = Serial.encode( model )

            # Generate SHA3-256 code for an encoded model.

            code = Serial.code( y )

            z = Serial.decode( y )

            # Decode a dictionary instance from JSON.

            z = Serial.decode( '{ "a" : 1.0, "b" : 2.0, "c" : 3.14159 }' )

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-07-13.

    **Definition**

"""

import base64
import gzip
import hashlib
import jsonpickle
import jsonpickle.ext.numpy
import jsonpickle.ext.pandas
import re


class Serial( object ) :

    """ Serial service, with JSON or BSON, base-85 encoded gzip JSON, format.
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
    def decode( state : str, compress : bool = False, encoding : str = 'utf_8', clean : bool = False ) -> any :

        """ Decodes an instance or collection from JSON or BSON, base-85
            encoded gzip JSON, state.  Encoding may be specified if an
            alternative to UTF-8 is required.  Python style docstring and line
            comments may be cleaned, though line comments must be terminated by
            a new line.

            Arguments :

                state : str.

                compress : bool.

                encoding : str.

                clean : bool - clean comments.

            Returns :

                instance : any.
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
    def encode( instance : any, compress : bool = False, encoding : str = 'utf_8' ) -> str :

        """ Encodes JSON or BSON, base-85 encoded gzip JSON, state from an
            instance or collection.  Encoding may be specified if an
            alternative to UTF-8 is required.

            Arguments :

                instance : any.

                compress : bool.

                encoding : str.

            Returns :

                state : str.
        """

        if ( not encoding ) :

            raise ValueError( f'Encoding = {encoding}' )

        state = jsonpickle.encode( instance, separators = ( ',', ':' ) )

        if ( compress ) :

            state = str( base64.b85encode( gzip.compress( bytes( state, encoding ) ) ), encoding )

        return state
