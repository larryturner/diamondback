""" **Description**

        A diversity model realizes the selection and retention of a state as a
        finite collection of observations extracted from an incident signal, to
        maximize a minimum distance between any members of a state, according to
        a specified classification or distance metric.

        A diversity model is an opportunistic unsupervised learning model which
        typically improves condition and numerical accuracy and reduces storage
        relative to alternative approaches including generalized linear inverse.

        A factory is defined to facilitate construction of an instance, defining
        a state array of a specified order.  A stationary dimension is inferred
        through observation.  An instance, classification, and order are specified.

        Classification is in ( 'Chebyshev', 'Euclidean', 'Geometric', 'Manhattan' ).

        * | 'Chebyshev' distance is an L-infinity norm, a maximum absolute difference
          | in any dimension.

        * | 'Euclidean' distance is an L-2 norm, a square root of a sum of squared
          | differences in each dimension.

        * | 'Geometric' distance is a ordered root of a product of absolute differences
          | in each dimension.

        * | 'Manhattan' distance is an L-1 norm, a sum of absolute differences in each
          | dimension.

    **Example**

        ::

            from diamondback.models.DiversityModel import DiversityModel


            # Create an instance from a Factory with constraints.

            obj = DiversityModel.Factory.instance( typ = DiversityModel, classification = 'Euclidean', order = 4 )

            # Model an incident signal and extract a state.

            x = numpy.random.rand( 2, 32 )

            y = obj.model( x )

            s = obj.s

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-02-08.

    **Definition**

"""

from diamondback.interfaces.IClear import IClear
from diamondback.interfaces.IEqual import IEqual
from diamondback.interfaces.IS import IS
import numpy


class DiversityModel( IClear, IS, IEqual ) :

    """ Diversity model.
    """

    class Factory( object ) :

        """ Factory.
        """

        _distance = { 'Chebyshev' : lambda x, y : max( abs( x - y ) ),
                      'Euclidean' : lambda x, y : sum( ( x - y ) ** 2 ) ** 0.5,
                      'Geometric' : lambda x, y : numpy.prod( abs( x - y ) ) ** ( 1.0 / len( x ) ),
                      'Manhattan' : lambda x, y : sum( abs( x - y ) ) }

        @classmethod
        def instance( cls, typ, classification, order ) :

            """ Constructs an instance.

                Arguments :

                    typ - Type derived from DiversityModel ( type ).

                    classification - Classification in ( 'Chebyshev', 'Euclidean', 'Geometric', 'Manhattan' ) ( str ).

                    order - Order ( int ).

                Returns :

                    instance - Instance ( typ( ) ).
            """

            if ( ( not typ ) or ( not issubclass( typ, DiversityModel ) ) ) :

                raise ValueError( 'type = ' + str( typ ) )

            if ( ( not classification ) or ( classification not in DiversityModel.Factory._distance ) ) :

                raise ValueError( 'classification = ' + str( classification ) )

            if ( order <= 0 ) :

                raise ValueError( 'order = ' + str( order ) )

            return typ( DiversityModel.Factory._distance[ classification ], order )

    def __eq__( self, other ) :

        """ Evaluates equality condition.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self._distance == other._distance ) and ( numpy.isclose( self._diversity, other._diversity ) ) )

    def __init__( self, distance, order ) :

        """ Initializes an instance.

            Arguments :

                distance - Distance ( method ).

                order - Order ( int ).
        """

        if ( ( not distance ) or ( isinstance( distance, str ) ) ) :

            raise ValueError( 'distance = ' + str( distance ) )

        super( ).__init__( )

        self._distance, self._diversity, self._s = distance, 0.0, numpy.zeros( ( 0, order + 1 ) )

    def clear( self ) :

        """ Clears an instance.
        """

        self._diversity, self._s = 0.0, numpy.zeros( ( 0, self.s.shape[ 1 ] ) )

    def model( self, x ) :

        """ Models an incident signal and produces a reference signal.

            Arguments :

                x - Incident signal ( array( float ), list( float ) ).

            Returns :

                y = Diversity ( array( float ) ).
        """

        if ( ( not numpy.isscalar( x ) ) and ( not isinstance( x, numpy.ndarray ) ) ) :

            x = numpy.array( list( x ) )

        if ( ( len( x.shape ) > 2 ) or ( len( x ) == 0 ) ) :

            raise ValueError( 'x = ' + str( x ) )

        if ( len( x.shape ) < 2 ) :

            rows, cols = 1, x.shape[ 0 ]

        else :

            rows, cols = x.shape

        if ( not self.s.shape[ 0 ] ) :

            self._s = numpy.zeros( ( rows, self.s.shape[ 1 ] ) ) + numpy.finfo( float ).max

        if ( ( rows != self.s.shape[ 0 ] ) or ( cols <= 0 ) ) :

            raise ValueError( 'rows = ' + str( rows ) + ' cols = ' + str( cols ) )

        cc = 0

        for jj in range( 0, self.s.shape[ 1 ] ) :

            if ( numpy.isclose( self.s[ 0, jj ], numpy.finfo( float ).max ) ) :

                break

            cc += 1

        y = numpy.zeros( cols )

        for jj in range( 0, cols ) :

            if ( cc < self.s.shape[ 1 ] ) :

                self.s[ :, cc ] = x[ :, jj ]

                cc += 1

            else :

                v, ii = self._diversity, -1

                for kk in range( 0, cc ) :

                    u, s = float( 'inf' ), numpy.array( self.s )

                    s[ :, kk ] = x[ :, jj ]

                    for uu in range( 0, cc - 1 ) :

                        for vv in range( uu + 1, cc ) :

                            d = self._distance( s[ :, uu ], s[ :, vv ] )

                            if ( d < u ) :

                                u = d

                    if ( u > v ) :

                        v, ii = u, kk

                if ( v > self._diversity ) :

                    self._diversity, self.s[ :, ii ] = v, x[ :, jj ]

            y[ jj ] = self._diversity

        return y
