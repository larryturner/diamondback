""" **Description**
        A diversity model realizes the selection and retention of a state as a
        finite collection of observations extracted from an incident signal, to
        maximize a minimum distance between any members of a state, according to
        a specified style or distance metric.

        .. math::

            d_{k} = \\min(\\ d_{u,v}\\ )\\quad\\quad u, v \\in [\\ 0,\\ M\\ ),\\ u \\neq v

        .. math::

            d_{k} \\geq d_{n}\\qquad \\longrightarrow\\qquad d_{n} = d_{k}

        A diversity model is an opportunistic unsupervised learning model which
        typically improves condition and numerical accuracy and reduces storage
        relative to alternative approaches including generalized linear inverse.

        A state array of a specified order is defined.  A stationary dimension is
        inferred.  A style and order are specified.

        Style is in ( 'Chebyshev', 'Euclidean', 'Geometric', 'Manhattan' ).

        * | 'Chebyshev' distance is an L-infinity norm, a maximum absolute difference
          | in any dimension.

        .. math::

            d_{u,v} = \\max(\\ |\\ \\vec{x_{u}} - \\vec{x_{v}}\\ |\\ )

        * | 'Euclidean' distance is an L-2 norm, a square root of a sum of squared
          | differences in each dimension.

        .. math::

            d_{u,v} = \\matrix{\\sum_{i=0}^{N}(\\ |\\ \\vec{x_{u,i}} - \\vec{x_{v,i}}\\ )^2|}^{0.5}

        * | 'Geometric' distance is a ordered root of a product of absolute differences
          | in each dimension.

        .. math::

            d_{u,v} = \\prod_{i=0}^{N}{(\\ |\\ \\vec{x_{u,i}} - \\vec{x_{v,i}}\\ |\\ )}^{\\frac{1}{N}}

        * | 'Manhattan' distance is an L-1 norm, a sum of absolute differences in each
          | dimension.

        .. math::

            d_{u,v} = \\sum_{i=0}^{N}{\\ (\\ |\\ \\vec{x_{u}} - \\vec{x_{v}}\\ |\\ )\\ }

    **Example**

        .. code-block:: python

            from diamondback import DiversityModel

            # Create an instance.

            obj = DiversityModel( style = 'Euclidean', order = 4 )

            # Learn an incident signal and extract a state.

            x = numpy.random.rand( 32, 2 )
            y = obj.learn( x )
            s = obj.s

    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2024 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, AI Hub, 2018-02-08.
"""

from typing import List, Union
import numpy

class DiversityModel( object ) :

    """ Diversity model.
    """

    DISTANCE = dict( Chebyshev = lambda x, y : max( abs( x - y ) ),
                     Euclidean = lambda x, y : sum( ( x - y ) ** 2 ) ** 0.5,
                     Geometric = lambda x, y : numpy.prod( abs( x - y ) ) ** ( 1.0 / len( x ) ),
                     Manhattan = lambda x, y : sum( abs( x - y ) ) )
    STYLE = tuple( DISTANCE.keys( ) )

    @property
    def s( self ) :
        return self._s

    @s.setter
    def s( self, s : Union[ List, numpy.ndarray ] ) :
        self._s = s

    def __init__( self, style : str, order : int ) -> None :

        """ Initialize.

            Arguments :
                style : str - in ( 'Chebyshev', 'Euclidean', 'Geometric', 'Manhattan' ).
                order : int.
        """

        style = style.title( )
        if ( style not in DiversityModel.STYLE ) :
            raise ValueError( f'style = {style} Expected Style in {DiversityModel.STYLE}' )
        if ( order < 0 ) :
            raise ValueError( f'Order = {order} Expected Order in [ 0, inf )' )
        super( ).__init__( )
        self._distance = DiversityModel.DISTANCE[ style ]
        self._diversity = 0.0
        self._s = numpy.zeros( ( order + 1, 0 ) )

    def clear( self ) -> None :

        """ Clears an instance.
        """

        self._diversity = 0.0
        self.s = numpy.zeros( ( self.s.shape[ 1 ], 0 ) )

    def learn( self, x : Union[ List, numpy.ndarray ] ) -> numpy.ndarray :

        """ Learns an incident signal and produces a reference signal.

            Arguments :
                x : Union[ List, numpy.ndarray ] - incident signal.

            Returns :
                y : numpy.ndarray - diversity.
        """

        if ( not isinstance( x, numpy.ndarray ) ) :
            x = numpy.array( list( x ) )
        if ( ( len( x.shape ) != 2 ) or ( not all( x.shape ) ) ) :
            raise ValueError( f'X = {x}' )
        if ( not self.s.shape[ 1 ] ) :
            self.s = numpy.zeros( ( self.s.shape[ 0 ], x.shape[ 1 ] ) ) + numpy.finfo( float ).max
        if ( x.shape[ 1 ] != self.s.shape[ 1 ] ) :
            raise ValueError( f'X = {x.shape} S = {self.s.shape}' )
        cc = 0
        for ii in range( 0, self.s.shape[ 0 ] ) :
            if ( numpy.isclose( self.s[ ii, 0 ], numpy.finfo( float ).max ) ) :
                break
            cc += 1
        y = numpy.zeros( x.shape[ 0 ] )
        for ii in range( 0, x.shape[ 0 ] ) :
            if ( cc < self.s.shape[ 0 ] ) :
                self.s[ cc, : ] = x[ ii, : ]
                cc += 1
            else :
                v, jj = self._diversity, -1
                for kk in range( 0, cc ) :
                    u, s = numpy.inf, numpy.array( self.s )
                    s[ kk, : ] = x[ ii, : ]
                    for uu in range( 0, cc - 1 ) :
                        for vv in range( uu + 1, cc ) :
                            d = self._distance( s[ uu, : ], s[ vv, : ] )
                            if ( d < u ) :
                                u = d
                    if ( u > v ) :
                        v, jj = u, kk
                if ( v > self._diversity ) :
                    self._diversity, self.s[ jj, : ] = v, x[ ii, : ]
            y[ ii ] = self._diversity
        return y
