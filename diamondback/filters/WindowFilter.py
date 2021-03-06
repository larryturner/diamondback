""" **Description**

        A window filter realizes a discrete difference equation as a function
        of a forward coefficient array of a specified order, consuming an
        incident signal and producing a reference signal.

        .. math::

            y_{n} = b_{n}\ x_{n}

        A factory is defined to facilitate construction of an instance,
        defining a forward coefficient array of a specified order.  An
        instance, classification, order, and normalization are specified.

        Classification is in ( 'Blackman', 'Hamming', 'Hann', 'Kaiser' ).

        * | 'Blackman' filters demonstrate low resolution and spectral leakage
          | with improved rate of attenuation.

        * | 'Hamming' filters demonstrate minimal nearest side lobe magnitude
          | response.

        * | 'Hann' filters demonstrate high resolution and spectral leakage.

        * | 'Kaiser' filters demonstrate flexible resolution and spectral
          | leakage dependent upon a beta value of a Bessel function of the
          | first kind, with beta equal to 7.0.

        Normal condition scales a forward coefficient array to electively
        compensate for energy loss.

        .. math::

            b_{n} = b_{n}\ \\frac{ N }{ \sum_{0}^{N-1}\ |\ b_{n}\ |}

    **Example**

        ::

            from diamondback import ComplexExponentialFilter, WindowFilter
            import numpy


            # Create an instance from a Factory with constraints.

            obj = WindowFilter.Factory.instance( typ = WindowFilter, classification = 'Hann', order = 15, normal = True )

            # Filter an incident signal.

            x = ComplexExponentialFilter( 0.0 ).filter( numpy.ones( len( obj.b ) ) * 0.1 ).real

            y = obj.filter( x )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-04-13.

    **Definition**

"""

from diamondback.interfaces.IB import IB
from diamondback.interfaces.IEqual import IEqual
import numpy
import scipy.signal


class WindowFilter( IB, IEqual ) :

    """ Window filter.
    """

    class Factory( object ) :

        """ Factory.
        """

        _classification = ( 'Blackman', 'Hamming', 'Hann', 'Kaiser' )

        @classmethod
        def instance( cls, typ : type, classification : str, order : int, normal : bool = True ) -> any :

            """ Constructs an instance.

                Arguments :

                    typ - Type derived from WindowFilter ( type ).

                    classification - Classification in ( 'Blackman', 'Hamming', 'Hann', 'Kaiser' ) ( str ).

                    order - Order ( int ).

                    normal - Normal condition ( bool ).

                Returns :

                    instance - Instance ( typ( ) ).
            """

            if ( ( not typ ) or ( not issubclass( typ, WindowFilter ) ) ) :

                raise ValueError( 'Type = ' + str( typ ) )

            if ( ( not classification ) or ( classification not in WindowFilter.Factory._classification ) ) :

                raise ValueError( 'Classification = ' + str( classification ) )

            if ( order < 0 ) :

                raise ValueError( 'Order = ' + str( order ) )

            if ( classification == 'Kaiser' ) :

                window = ( classification.lower( ), 7.0 )

            else :

                window = classification.lower( )

            b = scipy.signal.get_window( window, order + 1, False )

            if ( normal ) :

                b *= ( order + 1 ) / sum( abs( b ) )

            return typ( b )

    def __init__( self, b : any = numpy.ones( 1 ) ) -> None :

        """ Initialize.

            Arguments :

                b - Forward coefficient ( array( float ) ).
        """

        if ( ( numpy.isscalar( b ) ) or ( len( b.shape ) != 1 ) or ( len( b ) == 0 ) or ( not b.any( ) ) ) :

            raise ValueError( 'B = ' + str( b ) )

        super( ).__init__( )

        self.b = numpy.array( b )

    def filter( self, x : any ) -> any :

        """ Filters an incident signal and produces a reference signal.

            Arguments :

                x - Incident signal ( array( complex | float ), list( complex | float ) ).

            Returns :

                y - Reference signal ( array( complex | float ) ).
        """

        if ( ( not numpy.isscalar( x ) ) and ( not isinstance( x, numpy.ndarray ) ) ) :

            x = numpy.array( list( x ) )

        if ( ( len( x.shape ) != 1 ) or ( len( x ) != len( self.b ) ) ) :

            raise ValueError( 'X = ' + str( x ) )

        return self.b * x
