""" **Description**
        A Gaussian mixture model is a semi-supervised learning probabilistic
        model instance which uses maximum likelihood estimation, 
        regularization, and expectation maximization to maximize posterior
        probability and classify an incident signal.  Learns model instances
        of a specified order per class, where intra-class models capture
        mixture distributions. 

    **Example**
      
        ::
        
            from diamondback import GaussianMixtureModel

            # Create an instance.

            obj = GaussianMixtureModel( order = 10, index = 100 )

            # Learn an incident signal and predict classification.

            x, y = numpy.random.rand( 32, 2 ), numpy.random.randint( 0, 10, 32 )
            obj.learn( x, y )
            x = numpy.random.rand( 16, 2 )
            v = obj.predict( x )

    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2023 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, AI Hub, 2018-02-08.
"""

import numpy
import sklearn.mixture

class GaussianMixtureModel( object ) :
    
    """ Gaussian mixture model.
    """

    @property
    def index( self ) :
        return self._index

    @index.setter
    def index( self, index ) :
        if ( index < 1 ) :
            raise ValueError( f'Index = {index} Expected Index in [ 1, inf )' )
        self._index = index

    @property
    def order( self ) :
        return self._order

    @property
    def regularize( self ) :
        return self._regularize

    @regularize.setter
    def regularize( self, regularize : float ) :
        if ( regularize < 0.0 ) :
            raise ValueError( f'Regularize = {regularize} Expected Regularize in [ 0.0, inf )' )
        self._regularize = regularize

    @property
    def shape( self ) :
        return self._shape

    def __init__( self, order : int = 10, index : int = 100, regularize : float = 1.0e-1 ) -> None :

        """ Initialize.

            Arguments :
                order : int - mixture distributions per class.
                index : int - iterations.
                regularize : float - regularize.
        """

        if ( order < 1 ) :
            raise ValueError( f'Order = {order} Expected Order in [ 1, inf )' )
        if ( index < 1 ) :
            raise ValueError( f'Index = {index} Expected Index in [ 1, inf )' )
        if ( regularize < 0.0 ) :
            raise ValueError( f'Regularize = {regularize} Expected Regularize in [ 0.0, inf )' )
        self._data = [ ]
        self._index = index
        self._order = order
        self._regularize = regularize
        self._shape = ( )

    def learn( self, x : numpy.ndarray, y : numpy.ndarray ) -> None :

        """ Learns an incident signal with ground truth label and estimates inverse
            covariance and mean matrices to learn mixed distribution instances
            for each class.
        
            Arguments :
                x : numpy.ndarray ( batch, count ) - incident.
                y : numpy.ndarray ( batch ) - label.
        """

        if ( ( len( x.shape ) != 2 ) or ( not all( x.shape ) ) ) :
            raise ValueError( f'X = {x.shape}' )
        if ( len( y ) != x.shape[ 0 ] ) :
            raise ValueError( f'Y = {len( y )} Expected Y = {x.shape[ 0 ]}' )
        if ( not issubclass( y.dtype.type, numpy.integer ) ) :
            raise ValueError( f'Y = {y.dtype.type} Expected Y = {numpy.integer}' )
        self._data = [ ]
        self._shape = x[ 0 ].shape
        for ii in sorted( set( y ) ) :
            z = x[ numpy.where( y == ii )[ 0 ] ]
            m = sklearn.mixture.GaussianMixture( covariance_type = 'full', n_components = self.order, max_iter = self.index, reg_covar = self.regularize )
            m.fit( z )
            self._data.append( m )

    def predict( self, x : numpy.ndarray ) -> numpy.ndarray :

        """ Predicts an estimate of ground truth label from an incident signal
            and maximizes posterior probability of weighted intra-class mixed
            distributions.

            Predictions for each class are ranked and ordered by decending
            probability, and the initial prediction is the most likely class.
        
            Arguments :
                x : numpy.ndarray ( batch, count ) - data.

            Returns :
                v : numpy.ndarray ( batch, class ) - predict.
        """

        if ( not len( self._data ) ) :
            raise ValueError( f'Data = {self._data}' )
        if ( ( len( x.shape ) != 2 ) or ( not all( x.shape ) ) ) :
            raise ValueError( f'X = {x.shape}' )
        if ( x[ 0 ].shape != self._shape ) :
            raise ValueError( f'X = {x[ 0 ].shape} Expected X = {self._shape}' )
        if ( ( not len( self._data ) ) or ( not hasattr( self._data[ 0 ], 'precisions_' ) ) ) :
            raise RuntimeError( f'Model = {self._data} Not Trained' )
        v = numpy.zeros( ( x.shape[ 0 ], len( self._data ) ) )
        for jj in range( 0, len( v ) ) :
            for ii in range( 0, len( self._data ) ) :
                m = self._data[ ii ]
                for kk in range( 0, self.order ) :
                    i, u, w = m.precisions_[ kk ], m.means_[ kk ], m.weights_[ kk ]
                    v[ jj, ii ] += w * numpy.exp( -0.5 * max( ( x[ jj ] - u ) @ i @ ( x[ jj ] - u ).T, 0.0 ) )
        return numpy.fliplr( numpy.argsort( v, axis = 1 ) )
