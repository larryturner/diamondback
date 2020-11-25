""" **Description**

        A principal component model analyzes an incident signal to define
        transformation matrices which consume an incident signal to produce a
        reference signal, normalized and ordered to define orthogonal axes of
        descending variance.

        A principal component model is a supervised learning model which
        analyzes an incident signal representing a training set to learn a mean
        vector, standard deviation vector, and a collection of eigenvectors
        associated with an incident signal.

        .. math::

            \\vec{\mu_{i}} = \matrix{\ \\frac{\sum_{n=0}^{N}\\vec{x_{i,n}}}{N}}

        .. math::

            \\vec{\sigma_{i}} = \matrix{\ \\frac{\sum_{n=0}^{N}(\ \\vec{x_{i,n}} - \\vec{\mu_{i}}\ )^{2}}{N}}^{0.5}

        .. math::

            \Lambda_{n} = eig\matrix{\ cov\matrix{\ \matrix{\\frac{\ X_{n}^{T} - \\vec{\mu}\ }{\\vec{\sigma}}\ }\ }^{T}\ }^{T}

        An incident signal which is not a part of an inital training set is
        transformed without modifying a principal component model, by
        translation, normalization, and rotation to produce a reference signal
        which is a candidate for dimension reduction, in which higher order
        dimensions are discarded, reducing the order of the reference signal,
        while preserving significant and often sufficient information.

        .. math::

            Y_{n} = \Lambda_{n} \ \matrix{\\frac{\ X_{n}^{T} - \\vec{\mu}\ }{\\vec{\sigma}}\ }^{T}

        Principal component analysis and dimension reduction has application in
        clustering, classification, pattern recognition, and visualization.

    **Example**

        ::

            from diamondback import PrincipalComponentModel


            # Create an instance.

            obj = PrincipalComponentModel( )

            # Model an incident signal and extract eigenvalue, standard deviation, means, and rotation arrays.

            x = numpy.random.rand( 3, 32 )

            y = obj.model( x )

            e, s, u, v = obj.e, obj.s, obj.u, obj.v

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2019, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2019-01-25.

    **Definition**

"""

from diamondback.interfaces.IClear import IClear
from diamondback.interfaces.IEqual import IEqual
from diamondback.interfaces.IS import IS
import numpy


class PrincipalComponentModel( IClear, IS, IEqual ) :

    """ Principal component model.
    """

    @property
    def e( self ) :

        """ Eigenvalues ( array( float ) ).
        """

        return self._e

    @property
    def u( self ) :

        """ Mean ( array( float ) ).
        """

        return self._u

    @property
    def v( self ) :

        """ Rotation ( array( float ) ).
        """

        return self._v

    def __eq__( self, other : any ) -> bool :

        """ Equality.

            Arguments :

                other - other object ( object ).

            Returns :

                equality - Equality ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( numpy.allclose( self.u, other.u ) ) and ( numpy.isclose( self.v, other.v ) ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._e, self._s, self._u, self._v = numpy.array( [ ] ), numpy.array( [ ] ), numpy.array( [ ] ), numpy.array( [ ] )

    def clear( self ) -> None :

        """ Clears an instance.
        """

        self._e, self._s, self._u, self._v = numpy.array( [ ] ), numpy.array( [ ] ), numpy.array( [ ] ), numpy.array( [ ] )

    def model( self, x : any ) -> any :

        """ Models an incident signal and produces a reference signal.

            Arguments :

                x - Incident signal ( array( float ), list( float ) ).

            Returns :

                y - Reference signal ( array( float ) ).
        """

        if ( ( not numpy.isscalar( x ) ) and ( not isinstance( x, numpy.ndarray ) ) ) :

            x = numpy.array( list( x ) )

        if ( ( len( x.shape ) != 2 ) or ( len( x ) == 0 ) ) :

            raise ValueError( 'X = ' + str( x ) )

        if ( not len( self.s ) ) :

            self._s, self._u = x.std( 1 ), x.mean( 1 )

            z = ( ( x.T - self.u ) / self.s ).T

            self._e, self._v = numpy.linalg.eig( numpy.matmul( z, z.T ) / z.shape[ 1 ] )

            self._v = self._v.T

        else :

            z = ( ( x.T - self.u ) / self.s ).T

        rows, cols = x.shape

        if ( ( rows != len( self._u ) ) or ( ( rows, rows ) != self._v.shape ) or ( cols <= 0 ) ):

            raise ValueError( '{:30s}{:30s}'.format( 'Rows = ' + str( rows ), 'Columns = ' + str( cols ) ) )

        return numpy.matmul( self.v, z )
