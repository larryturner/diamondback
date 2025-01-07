""" **Description**
        A complex exponential filter produces a complex exponential reference
        signal from an incident signal equal to a specified normalized frequency.
        A normalized phase is specified.

        .. math::

            x_{n} = f_{n}

        .. math::

            \\phi_{n} = \\phi_{n-1} + x_{n}

        .. math::

            y_{n} = e^{\\ j\\ \\pi\\ \\phi_{n}}

    **Example**

        .. code-block:: python

            from diamondback import ComplexExponentialFilter
            import numpy

            complex_exponential_filter = ComplexExponentialFilter( phase = 0.0 )
            x = numpy.linspace( -1.0e-4, 1.0e-4, 128 ) + 0.1
            y = complex_exponential_filter.filter( x )

    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2024 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, AI Hub, 2018-01-31.
"""

import math
import numpy

class ComplexExponentialFilter( object ) :

    """ Complex exponential filter.
    """

    @property
    def phase( self ) :
        return self._phase

    @phase.setter
    def phase( self, phase : float ) :
        if ( ( phase < -1.0 ) or ( phase > 1.0 ) ) :
            raise ValueError( f'Phase = {phase} Expected Phase in [ -1.0, 1.0 ]' )
        self._phase = phase

    def __init__( self, phase : float = 0.0 ) -> None :

        """ Initialize.

            Arguments :
                phase : float - relative to pi in [ -1.0, 1.0 ].
        """

        if ( ( phase < -1.0 ) or ( phase > 1.0 ) ) :
            raise ValueError( f'Phase = {phase} Expected Phase in [ -1.0, 1.0 ]' )
        super( ).__init__( )
        self._phase = phase

    def filter( self, x : list | numpy.ndarray ) -> numpy.ndarray :

        """ Filters an incident signal and produces a reference signal.

            Arguments :
                x : list | numpy.ndarray - incident signal frequency normalized to Nyquist in [ -1.0, 1.0 ).

            Returns :
                y : numpy.ndarray - reference signal.
        """

        if ( not isinstance( x, numpy.ndarray ) ) :
            x = numpy.array( list( x ) )
        if ( ( numpy.iscomplex( x ).any( ) ) or ( not len( x ) ) or ( abs( x ) > 1.0 ).any( ) ) :
            raise ValueError( f'X = {x}' )
        y = numpy.zeros( len( x ), complex )
        phase = self.phase
        for ii in range( 0, len( x ) ) :
            y[ ii ] = numpy.exp( 1j * math.pi * phase )
            phase += x[ ii ]
        phase = numpy.fmod( phase, 2.0 )
        if ( abs( phase ) > 1.0 ) :
            phase -= numpy.sign( phase ) * 2.0
        self.phase = phase
        return y
