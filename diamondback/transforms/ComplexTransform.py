""" **Description**

        A complex transform converts a three-phase real signal to a complex
        signal, or converts a complex signal to a three-phase real signal, in
        equivalent and reversible representations.  A neutral condition is
        specified.

        Singleton.

        .. math::

            \gamma = \scriptsize{ \matrix{ 1 & \\frac{-1}{2} & \\frac{-1}{2}\cr 0 & \\frac{3^{0.5}}{2} & \\frac{-3^{0.5}}{2}\cr 1 & 1 & 1 } }

        .. math::

            \\alpha = \matrix{\\frac{1}{3}}^{0.5}\ e^{\ -j\ \\frac{\pi}{6}\ }

        * Complex - Three-Phase.

        .. math::

            y_{n} = \matrix{ x^{T}_{n}\ \gamma\ }\ \scriptsize{[\ \matrix{ 1 & j & 0 }\ ]^{T}}

        .. math::

            \overline{\scriptsize{Neutral}}\ \qquad\longrightarrow\qquad y_{n} = y_{n}\ \\alpha

        * Three-Phase - Complex.

        .. math::

            \overline{\scriptsize{Neutral}}\ \qquad\longrightarrow\qquad x_{n} = \\frac{x_{n}}{\\alpha}

        .. math::

            y_{n} = \matrix{\ \matrix{ \gamma^{T}\gamma }^{-1}\ \gamma^{T}\ \scriptsize{[\ \matrix{ real(\ x_{n}\ ) & imag(\ x_{n}\ ) & 0 }\ ]^{T}}}^{T}

    **Example** ::

        from diamondback.filters.ComplexExponentialFilter import ComplexExponentialFilter
        from diamondback.transforms.ComplexTransform import ComplexTransform
        import numpy


        x = ComplexExponentialFilter( 0.0 ).filter( numpy.linspace( -1.0e-4, 1.0e-4, 128 ) + 0.1 )

        # Transform an incident signal, forward and inverse.

        y = ComplexTransform.transform( x, neutral = True )

        z = ComplexTransform.transform( y, neutral = True )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-01-26.

    **Definition**

"""

import math
import numpy


class ComplexTransform( object ) :

    """ Complex transform.
    """

    _coefficient = ( 2.0 / 3.0 ) * numpy.array( [ [ 1.0, -0.5, -0.5 ],
                                                  [ 0.0, 0.5 * ( 3.0 ** 0.5 ), -0.5 * ( 3.0 ** 0.5 ) ],
                                                  [ 1.0, 1.0, 1.0 ] ] )

    _gain = ( ( 1.0 / 3.0 ) ** 0.5 ) * numpy.exp( -1j * math.pi / 6.0 )

    @classmethod
    def transform( cls, x, neutral = True ) :

        """ Transforms a real three-phase or complex incident signal into a complex
            or three-phase reference signal.

            Arguments :

                x - Incident signal ( array( complex | float ), list( complex | float ) ).

                neutral - Neutral or line reference condition ( bool ).

            Returns :

                y - Reference signal ( array( complex | float ) ).
        """

        if ( ( not numpy.isscalar( x ) ) and ( not isinstance( x, numpy.ndarray ) ) ) :

            x = numpy.array( list( x ) )

        if ( ( len( x.shape ) > 2 ) or ( len( x ) == 0 ) ) :

            raise ValueError( 'x = ' + str( x ) )

        if ( len( x.shape ) < 2 ) :

            rows, cols = 1, x.shape[ 0 ]

        else :

            rows, cols = x.shape

        if ( ( ( rows != 1 ) and ( rows != 3 ) ) or ( cols <= 0 ) ) :

            raise ValueError( 'rows = ' + str( rows ) + ' cols = ' + str( cols ) )

        if ( rows == 1 ) :

            v = x

            if ( not neutral ) :

                v = x / ComplexTransform._gain

            y = numpy.matmul( numpy.linalg.inv( ComplexTransform._coefficient ), numpy.array( [ v.real, v.imag, numpy.zeros( cols ) ] ) )

        else :

            v = numpy.matmul( ComplexTransform._coefficient, x )

            y = v[ 0, : ] + 1j * v[ 1, : ]

            if ( not neutral ) :

                y *= ComplexTransform._gain

        return y
