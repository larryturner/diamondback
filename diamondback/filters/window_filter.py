""" **Description**
        A window filter realizes a discrete difference equation as a function
        of a forward coefficient array of a specified order, consuming an
        incident signal and producing a reference signal.

        .. math::

            y_{n} = b_{n}\\ x_{n}

        A forward coefficient array of a specified order is defined.  A
        style, order, and normalization are specified.

        Style is in ( 'Blackman', 'Hamming', 'Hann', 'Kaiser' ).

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

            b_{n} = b_{n}\\ \\frac{ N }{ \\sum_{0}^{N-1}\\ |\\ b_{n}\\ |}

    **Example**

        .. code-block:: python

            from diamondback import ComplexExponentialFilter, WindowFilter
            import numpy

            window_filter = WindowFilter( style = 'Hann', order = 15, normal = True )
            x = ComplexExponentialFilter( 0.0 ).filter( numpy.ones( len( window_filter.b ) ) * 0.1 ).real
            y = window_filter.filter( x )

    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2025 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, AI Hub, 2018-04-13.
"""

import numpy
import scipy.signal

class WindowFilter( object ) :

    """ Window filter.
    """

    STYLE = ( 'Blackman', 'Hamming', 'Hann', 'Kaiser' )

    @property
    def b( self ) :
        return self._b

    def __init__( self, style : str, order : int, normal : bool = True  ) -> None :

        """ Initialize.

            Arguments :
                style : str - in ( 'Blackman', 'Hamming', 'Hann', 'Kaiser' ).
                order : int.
                normal : bool.
        """

        style = style.title( )
        if ( style not in WindowFilter.STYLE ) :
            raise ValueError( f'style = {style} Expected Style in {WindowFilter.STYLE}' )
        if ( order < 0 ) :
            raise ValueError( f'Order = {order} Expected Order in [ 0, inf )' )
        if ( style == 'Kaiser' ) :
            window = ( style.lower( ), 7.0 )
        else :
            window = style.lower( )  # type: ignore
        super( ).__init__( )
        b = scipy.signal.get_window( window, order + 1, False )
        if ( normal ) :
            b *= ( order + 1 ) / sum( abs( b ) )
        self._b = numpy.array( b )

    def filter( self, x : list | numpy.ndarray ) -> numpy.ndarray :

        """ Filters an incident signal and produces a reference signal.

            Arguments :
                x : list | numpy.ndarray - incident signal.

            Returns :
                y : numpy.ndarray - reference signal.
        """

        if ( not isinstance( x, numpy.ndarray ) ) :
            x = numpy.array( list( x ) )
        if ( ( len( x.shape ) != 1 ) or ( len( x ) != len( self.b ) ) ) :
            raise ValueError( f'X = {x}' )
        return self.b * x
