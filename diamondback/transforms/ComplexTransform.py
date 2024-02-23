""" **Description**
        A complex transform converts a three-phase real signal to a complex
        signal, or converts a complex signal to a three-phase real signal, in
        equivalent and reversible representations.  A neutral condition is
        specified.

        Singleton.

        .. math::

            \\gamma = \\scriptsize{ \\matrix{ 1 & \\frac{-1}{2} & \\frac{-1}{2}\\cr 0 & \\frac{3^{0.5}}{2} & \\frac{-3^{0.5}}{2}\\cr 1 & 1 & 1 } }
            \\alpha = \\matrix{\\frac{1}{3}}^{0.5}\\ e^{\\ -j\ \\frac{\\pi}{6}\\ }

        Complex - Three-Phase.

        .. math::

            y_{n} = \\matrix{ x^{T}_{n}\\ \\gamma\\ }\ \\scriptsize{[\\ \\matrix{ 1 & j & 0 }\\ ]^{T}}
            \\overline{\\scriptsize{Neutral}}\\ \\qquad\\longrightarrow\\qquad y_{n} = y_{n}\\ \\alpha

        Three-Phase - Complex.

        .. math::

            \\overline{\\scriptsize{Neutral}}\\ \\qquad\\longrightarrow\\qquad x_{n} = \\frac{x_{n}}{\\alpha}
            y_{n} = \\matrix{\\ \\matrix{ \\gamma^{T}\\gamma }^{-1}\\ \\gamma^{T}\\ \\scriptsize{[\\ \\matrix{ real(\\ x_{n}\\ ) & imag(\\ x_{n}\\ ) & 0 }\\ ]^{T}}}^{T}

    **Example**

        .. code-block:: python

            from diamondback import ComplexExponentialFilter, ComplexTransform
            import numpy

            x = ComplexExponentialFilter( 0.0 ).filter( numpy.linspace( -1.0e-4, 1.0e-4, 128 ) + 0.1 )

            # Transform an incident signal, forward and inverse.

            y = ComplexTransform.transform( x, neutral = True )
            z = ComplexTransform.transform( y, neutral = True )

    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2024 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, AI Hub, 2018-01-26.
"""

from typing import List, Union
import math
import numpy

class ComplexTransform( object ) :

    """ Complex transform.
    """

    COEFFICIENT = ( 2.0 / 3.0 ) * numpy.array( [ [ 1.0, -0.5, -0.5 ],
                                                 [ 0.0, 0.5 * ( 3.0 ** 0.5 ), -0.5 * ( 3.0 ** 0.5 ) ],
                                                 [ 1.0, 1.0, 1.0 ] ] )
    GAIN = ( ( 1.0 / 3.0 ) ** 0.5 ) * numpy.exp( -1j * math.pi / 6.0 )

    @classmethod
    def transform( cls, x : Union[ List, numpy.ndarray ], neutral : bool = True ) -> numpy.ndarray :

        """ Transforms a real three-phase or complex incident signal into a complex
            or three-phase reference signal.

            Arguments :
                x : Union[ List, numpy.ndarray ] - incident signal.
                neutral : bool.

            Returns :
                y : numpy.ndarray - reference signal.
        """

        if ( not isinstance( x, numpy.ndarray ) ) :
            x = numpy.array( list( x ) )
        if ( ( len( x.shape ) > 2 ) or ( len( x ) == 0 ) ) :
            raise ValueError( f'X = {x}' )
        if ( len( x.shape ) < 2 ) :
            rows, cols = 1, x.shape[ 0 ]
        else :
            rows, cols = x.shape
        if ( ( rows not in ( 1, 3 ) ) or ( cols <= 0 ) ) :
            raise ValueError( f'Rows = {rows} Columns = {cols} Expected Rows in ( 1, 3 ) and Columns in ( 0, inf )' )
        if ( rows == 1 ) :
            v = x
            if ( not neutral ) :
                v = x / ComplexTransform.GAIN
            y = numpy.matmul( numpy.linalg.inv( ComplexTransform.COEFFICIENT ), numpy.array( [ v.real, v.imag, numpy.zeros( cols ) ] ) )
        else :
            v = numpy.matmul( ComplexTransform.COEFFICIENT, x )
            y = v[ 0, : ] + 1j * v[ 1, : ]
            if ( not neutral ) :
                y *= ComplexTransform.GAIN
        return y
