""" **Description**
        An integral filter realizes a discrete difference equation which
        approximates a discrete integral as a function of a recursive coefficient
        array, a forward coefficient array, and a state array of a specified order,
        consuming an incident signal and producing a reference signal.  An integral
        is approximated relative to a sample.  An integral is electively approximated
        relative to a second by dividing a reference signal by an absolute sampling
        frequency.

        .. math::

            y_{n} = \\sum_{i = 1}^{N} a_{i} y_{n-i} + \\sum_{i = 0}^{N} b_{i} x_{n-i} = \\sum_{i = 1}^{N} (\\ a_{i} b_{0} + b_{i}\\ ) s_{i,n} + b_{0} x_{n}\\qquad a_{0} = 0

        .. math::

            s_{1,n+1} = \\sum_{i = 1}^{N} a_{i} s_{i,n} + x_{n}\\qquad\\quad s_{i,n+1} = s_{i-1,n}

        A frequency response is expressed as a function of a recursive coefficient
        array and a forward coefficient array.

        .. math::

                H_{z} = \\frac{\\sum_{i = 0}^{N} b_{i} z^{-i}}{{1 - \\sum_{i = 1}^{N} a_{i} z^{-i}}}

        A recursive coefficient array, forward coefficient array, and state array
        of a specified order are defined to satisfy specified constraints.  An
        instance and order are specified.

        .. math::

            y_{n} = \\frac{1}{f}\\ \\sum_{i=0}^{N} x_{n}\\quad\\quad\\quad\\quad\\scriptsize{ f = 1.0 }

        .. math::

            \\matrix{ a_{1,0} = \\scriptsize{ [ \\matrix{ 0 & 1 } ] } & b_{1,0} = \\scriptsize{ [ \\matrix{ 1 } ] } }\\quad\\quad\\scriptsize{ Rectangular }

        .. math::

            \\matrix{ a_{1,1} = \\scriptsize{ [ \\matrix{ 0 & 1 } ] } & b_{1,1} = \\scriptsize{ [ \\matrix{ 1 & 1 } ]\\ \\frac{1}{2} } }\\quad\\quad\\scriptsize{ Trapezoidal }

        .. math::

            \\matrix{ a_{1,2} = \\scriptsize{ [ \\matrix{ 0 & 1 } ] } & b_{1,2} = \\scriptsize{ [ \\matrix{ 1 & 4 & 1 } ]\\ \\frac{1}{6} } }\\quad\\quad\\scriptsize{ Simpson\\ 2 }

        .. math::

            \\matrix{ a_{1,3} = \\scriptsize{ [ \\matrix{ 0 & 1 } ] } & b_{1,3} = \\scriptsize{ [ \\matrix{ 1 & 3 & 3 & 1 } ]\\ \\frac{1}{8} } }\\quad\\quad\\scriptsize{ Simpson\\ 3 }

        .. math::

            \\matrix{ a_{1,4} = \\scriptsize{ [ \\matrix{ 0 & 1 } ] } & b_{1,4} = \\scriptsize{ [ \\matrix{ 7 & 32 & 12 & 32 & 7 } ]\\ \\frac{1}{90} } }\\quad\\quad\\scriptsize{ Newton\\ Coats }

    **Example**

        .. code-block:: python

            from diamondback import ComplexExponentialFilter, IntegralFilter
            import numpy

            # Create an instance.

            obj = IntegralFilter( order = 2 )

            # Filter an incident signal.

            x = ComplexExponentialFilter( 0.0 ).filter( numpy.ones( 128 ) * 0.1 ).real
            y = obj.filter( x )

    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2024 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, AI Hub, 2018-02-06.
"""

from diamondback.filters.IirFilter import IirFilter
from typing import List, Union
import numpy

class IntegralFilter( IirFilter ) :

    """ Integral filter.
    """

    B = ( numpy.array( [ 1.0 ] ),
          numpy.array( [ 1.0, 1.0 ] ) * ( 1.0 / 2.0 ),
          numpy.array( [ 1.0, 4.0, 1.0 ] ) * ( 1.0 / 6.0 ),
          numpy.array( [ 1.0, 3.0, 3.0, 1.0 ] ) * ( 1.0 / 8.0 ),
          numpy.array( [ 7.0, 32.0, 12.0, 32.0, 7.0 ] ) * ( 1.0 / 90.0 ) )

    def __init__( self, order : int ) -> None :

        """ Initialize.

            Arguments :
                order : int.
        """

        if ( ( order < 0 ) or ( order >= len( IntegralFilter.B ) ) ) :
            raise ValueError( f'Order = {order} Expected Order in [ 0, {len( IntegralFilter.B )} )' )
        super( ).__init__( a = numpy.array( [ 0.0, 1.0 ] ), b = IntegralFilter.B[ order ] )

    def filter( self, x : Union[ List, numpy.ndarray ] ) -> numpy.ndarray :

        """ Filters an incident signal and produces a reference signal.

            Arguments :
                x : Union[ List, numpy.ndarray ] - incident signal.

            Returns :
                y : numpy.ndarray - reference signal.
        """

        return super( ).filter( x )
