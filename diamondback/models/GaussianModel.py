""" **Description**
        A Gaussian model is a supervised learning probabilistic model instance
        which uses maximum likelihood estimation and regularization to maximize
        posterior probability and classify an incident signal.  Learns one
        distribution instance per class.

    **Example**
      
        ::
        
            from diamondback import GaussianModel

            # Create an instance.

            obj = GaussianModel( )

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

from typing import Any, Dict, List
import numpy

class GaussianModel( object ) :

    """ Gaussian model.
    """

    @property
    def regularize( self ) :

        """ regularize : float.
        """

        return self._regularize

    @regularize.setter
    def regularize( self, regularize : float ) :

        if ( regularize < 0.0 ) :
            raise ValueError( f'Regularize = {regularize} Expected Regularize in [ 0.0, inf )' )
        self._regularize = regularize

    @property
    def shape( self ) :

        """ shape : Tuple[ Any ].
        """

        return self._shape
        
    def __init__( self, regularize : float = 1.0e-1 ) -> None :

        """ Initialize.

            Arguments :
                regularize : float - regularize.
        """

        if ( regularize < 0.0 ) :
            raise ValueError( f'Regularize = {regularize} Expected Regularize in [ 0.0, inf )' )
        self._data : List[ Dict[ Any, Any ] ] = [ ]
        self._regularize = regularize
        self._shape = ( )

    def learn( self, x : numpy.ndarray, y : numpy.ndarray ) -> None :

        """ Learns an incident signal with ground truth label and estimates inverse
            covariance and mean matrices to learn a distribution instance for
            each class.
        
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
        r = self.regularize * numpy.identity( x.shape[ 1 ] )
        for ii in sorted( set( y ) ) :
            z = x[ numpy.where( y == ii )[ 0 ] ]
            u = z.mean( 0 )
            i = numpy.linalg.inv( ( ( z - u ).T @ ( z - u ) / z.shape[ 1 ] ) + r )
            self._data.append( dict( covariancei = i, mean = u ) )

    def predict( self, x : numpy.ndarray ) -> numpy.ndarray :

        """ Predicts an estimate of ground truth label from an incident signal
            and maximizes posterior probability.
            
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
        if ( not len( self._data ) ) :
            raise RuntimeError( f'Model = {self._data} Not Trained' )
        v = numpy.zeros( ( x.shape[ 0 ], len( self._data ) ) )
        for jj in range( 0, len( v ) ) :
            for ii in range( 0, len( self._data ) ) :
                m = self._data[ ii ]
                i, u = m[ 'covariancei' ], m[ 'mean' ]
                v[ jj, ii ] = max( ( x[ jj ] - u ) @ i @ ( x[ jj ] - u ).T, 0.0 )
        return numpy.argsort( v, axis = 1 )
