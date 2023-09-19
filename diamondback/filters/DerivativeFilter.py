""" **Description**
        A derivative filter realizes a discrete difference equation which
        approximates a discrete derivative as a function of a forward coefficient
        array and a state array of a specified order, consuming an incident signal
        and producing a reference signal.  A derivative is approximated relative
        to a sample.  A derivative is electively approximated relative to a second
        by multiplying a reference signal by an absolute sampling frequency raised
        to a derivative power.

        .. math::
            y_{n} = \\sum_{i = 0}^{N} b_{i} x_{n-i} = \\sum_{i = 1}^{N} b_{i} s_{i,n} + b_{0} x_{n}
            s_{1,n+1} = x_{n}\\qquad\\quad s_{i,n+1} = s_{i-1,n}

        A frequency response is expressed as a function of a forward coefficient
        array.

        .. math::
            H_{z} = \\sum_{i = 0}^{N} b_{i} z^{-i}

        A forward coefficient array and a state array of a specified order are
        defined, to satisfy specified constraints.  A derivative, and order are
        specified.

        .. math::
            y_{n} = f^{D}\\ \\frac{x_{n}}{D}\\quad\\quad\\quad\\quad\\scriptsize{ f = 1.0 }

        .. math::
            b_{1,1} = \\scriptsize{ [ \\matrix{ 1 & -1 } ] }

        .. math::
            b_{1,2} = \\scriptsize{ [ \\matrix{ 1 & 0 & -1 } ]\\ \\frac{1}{2} }

        .. math::
            b_{1,4} = \\scriptsize{ [ \\matrix{ -1 & 8 & 0 & -8 & 1 } ]\\ \\frac{1}{12} }

        .. math::
            b_{2,2} = \\scriptsize{ [ \\matrix{ 1 & -2 & 1 } ] }

        .. math::
            b_{2,4} = \\scriptsize{ [ \\matrix{ 1 & 0 & -2 & 0 & 1 } ]\\ \\frac{1}{4} }

        .. math::
            b_{2,6} = \\scriptsize{ [ \\matrix{ -1 & 8 & 1 & -16 & 1 & 8 & -1 } ]\\ \\frac{1}{24} }

        .. math::
            b_{2,8} = \\scriptsize{ [ \\matrix{ 1 & -16 & 64 & 16 & -130 & 16 & 64 & -16 & 1 } ]\\ \\frac{1}{144} }

        .. math::
            b_{3,4} = \\scriptsize{ [ \\matrix{ 1 & -2 & 0 & 2 & -1 } ]\\ \\frac{1}{2} }

        .. math::
            b_{3,6} = \\scriptsize{ [ \\matrix{ 1 & 0 & -3 & 0 & 3 & 0 & 1 } ]\\ \\frac{1}{8} }

        .. math::
            b_{3,8} = \\scriptsize{ [ \\matrix{ -1 & 8 & 2 & -24 & 0 & 24 & -2 & -8 & 1 } ]\\ \\frac{1}{48} }

    **Example**

        ::

            from diamondback import ComplexExponentialFilter, DerivativeFilter
            import numpy

            # Create an instance.

            obj = DerivativeFilter( derivative = 1, order = 2 )

            # Filter an incident signal.

            x = ComplexExponentialFilter( 0.0 ).filter( numpy.ones( 128 ) * 0.1 ).real
            obj.reset( x[ 0 ] )
            y = obj.filter( x )

    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2023 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, AI Hub, 2018-02-06.
"""

from diamondback.filters.FirFilter import FirFilter
from typing import List, Union
import numpy

class DerivativeFilter( FirFilter ) :

    """ Derivative filter.
    """

    B = { 1 : { 1 : numpy.array( [ 1.0, -1.0 ] ),
                2 : numpy.array( [ 1.0, 0.0, -1.0 ] ) * ( 1.0 / 2.0 ),
                4 : numpy.array( [ -1.0, 8.0, 0.0, -8.0, 1.0 ] ) * ( 1.0 / 12.0 ) },
          2 : { 2 : numpy.array( [ 1.0, -2.0, 1.0 ] ),
                4 : numpy.array( [ 1.0, 0.0, -2.0, 0.0, 1.0 ] ) * ( 1.0 / 4.0 ),
                6 : numpy.array( [ -1.0, 8.0, 1.0, -16.0, 1.0, 8.0, -1.0 ] ) * ( 1.0 / 24.0 ),
                8 : numpy.array( [ 1.0, -16.0, 64.0, 16.0, -130.0, 16.0, 64.0, -16.0, 1.0 ] ) * ( 1.0 / 144.0 ) },
          3 : { 4 : numpy.array( [ 1.0, -2.0, 0.0, 2.0, -1.0 ] ) * ( 1.0 / 2.0 ),
                6 : numpy.array( [ 1.0, 0.0, -3.0, 0.0, 3.0, 0.0, -1.0 ] ) * ( 1.0 / 8.0 ),
                8 : numpy.array( [ -1.0, 8.0, 2.0, -24.0, 0.0, 24.0, -2.0, -8.0, 1.0 ] ) * ( 1.0 / 48.0 ) } }

    def __init__( self, derivative : int, order : int ) -> None :

        """ Initialize.

            Arguments :
                derivative : int - in [ 1, 3 ].
                order : int.
        """

        if ( derivative not in DerivativeFilter.B ) :
            raise ValueError( f'Derivative = {derivative} Expected Derivative in {tuple( DerivativeFilter.B.keys( ) )}' )
        if ( order not in DerivativeFilter.B[ derivative ] ) :
            raise ValueError( f'Order = {order} Expected Order in {tuple( DerivativeFilter.B[ derivative ].keys( ) )}' )
        super( ).__init__( b = DerivativeFilter.B[ derivative ][ order ] )

    def filter( self, x : Union[ List, numpy.ndarray ] ) -> numpy.ndarray :

        """ Filters an incident signal and produces a reference signal.

            Arguments :
                x : Union[ List, numpy.ndarray ] - incident signal.

            Returns :
                y : numpy.ndarray - reference signal.
        """

        return super( ).filter( x )
