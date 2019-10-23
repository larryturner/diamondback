""" **Description**

        A rank filter realizes a nonlinear morphological operator consuming an
        incident signal, sorting, indexing, and selecting over a sliding window
        of a specified order, and producing a reference signal.

        Simple morphological operations include dilation, which defines a rank
        index equal to zero, erosion, which defines a rank index equal to order,
        and median, which defines a rank index equal to order divided by two
        for even order.  Compound morphological operations include close,
        consisting of sequential dilation and erosion, and open, consisting of
        sequential erosion and dilation.  An order and rank are specified.

        .. math::

            y_{n} = sort(\ x_{n-N+1\ :\ n}\ )[\ i\ ]

    **Example**

        ::

            from diamondback.filters.RankFilter import RankFilter
            import numpy


            # Create an instance with rank and order.

            obj = RankFilter( rank = 4, order = 4 )

            # Filter an incident signal.

            x = numpy.concatenate( ( numpy.ones( 1 ), numpy.zeros( 10 ), numpy.ones( 4 ), numpy.zeros( 2 ), numpy.ones( 5 ), numpy.zeros( 6 ) ) )

            obj.reset( x[ 0 ] )

            y = obj.filter( x )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-31.

    **Definition**

"""

from diamondback.filters.FirFilter import FirFilter
import numpy


class RankFilter( FirFilter ) :

    """ Rank filter.
    """

    @property
    def rank( self ) :

        """ Rank in [ 0, order ] ( int ).
        """

        return self._rank

    @rank.setter
    def rank( self, rank ) :

        if ( ( rank < 0 ) or ( rank > ( len( self.s ) - 1 ) ) ) :

            raise ValueError( 'Rank = ' + str( rank ) )

        self._rank = rank

    def __eq__( self, other ) :

        """ Evaluates equality condition.

            Arguments :

                other - Other object ( object ).

            Returns :

                equality - Equality condition ( bool ).
        """

        return ( ( super( ).__eq__( other ) ) and ( self.rank == other.rank ) )

    def __init__( self, rank, order ) :

        """ Initializes an instance.

            Arguments :

                rank - Rank in [ 0, order ] ( int ).

                order - Order ( int ).
        """

        if ( ( rank < 0 ) or ( rank > order ) ) :

            raise ValueError( '{:30s}{:30s}'.format( 'Rank = ' + str( rank ), 'Order = ' + str( order ) ) )

        super( ).__init__( numpy.ones( order + 1 ) / ( order + 1 ) )

        self._rank = rank

    def filter( self, x, d = None ) :

        """ Filters an incident signal and produces a reference signal.

            Arguments :

                x - Incident signal ( array( complex | float ), list( complex | float ) ).

            Returns :

                y - Reference signal ( array( complex | float ) ).
        """

        if ( ( not numpy.isscalar( x ) ) and ( not isinstance( x, numpy.ndarray ) ) ) :

            x = numpy.array( list( x ) )

        if ( ( len( x.shape ) != 1 ) or ( len( x ) == 0 ) ) :

            raise ValueError( 'X = ' + str( x ) )

        y = numpy.zeros( len( x ), type( x[ 0 ] ) )

        for ii in range( 0, len( x ) ) :

            self.s[ 0 ] = x[ ii ]

            y[ ii ] = self.s[ numpy.argsort( abs( self.s ) ) ][ self.rank ]

            if ( len( self.s ) > 1 ) :

                self.s[ 1 : ] = self.s[ : -1 ]

        return y
