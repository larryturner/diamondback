""" **Description**
        A power spectrum transform converts a real or complex discrete-time
        incident signal to a real discrete-frequency reference signal, which
        estimates a mean power density of the incident signal relative to
        frequency.  A forward coefficient array is specified to define a
        window filter.

        Singleton.

        A power spectrum transform is constructed by estimating a mean power
        from a collection of Fourier transforms of an incident signal, over a
        sliding window defined by a forward coefficient array which defines a
        window filter.  An index specifies a sample interval, or a
        non-overlapping stride, between successive operations.

        .. math::
            v_{i,k} = \\frac{1}{N}\\ \\sum_{n = 0}^{N-1} b_{n} x_{n+i\\ I} e^{ \\frac{\\ -j\\ \\pi\\ k \\ n}{N} }

        .. math::
            y_{k} = \\frac{1}{C}\\ \\sum_{i = 0}^{C-1} v_{i,k} v^{*}_{i,k}

        A spectrogram may be electively defined such that the collection of
        Fourier transforms is preserved to construct a time frequency
        representation of the power spectrum.

        A power spectrum transform is normalized by incident signal length and
        forms a contiguous sequence corresponding to a linear and increasing
        normalized frequency.

        .. math::
            f_{k} = \\ 2\ \\frac{k}{N}

        An incident signal length is inversely proportional to a normalized
        frequency resolution.

        .. math::
            N = \\frac{2}{R}

    **Example**
       
        ::
        
            from diamondback import ComplexExponentialFilter, PowerSpectrumTransform
            import numpy

            x = ComplexExponentialFilter( 0.0 ).filter( numpy.linspace( 0.12, 0.23, 1024 ) ) * numpy.random.rand( 1 )[ 0 ]
            b = WindowFilter( 'Hann', 128 - 1 ).b

            # Transform an incident signal.

            y, f = PowerSpectrumTransform.transform( x, b = b, index = len( b ) // 2 )

    **License**
        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_
        © 2018 - 2023 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**
        Larry Turner, Schneider Electric, AI Hub, 2018-04-13.
"""

from diamondback.transforms.FourierTransform import FourierTransform
from typing import List, Tuple, Union
import numpy

class PowerSpectrumTransform( object ) :

    """ Power spectrum transform.
    """

    @staticmethod
    def transform( x : Union[ List, numpy.ndarray ], b : Union[ List, numpy.ndarray ], index : int, spectrogram : bool = False ) -> Tuple[ numpy.ndarray, numpy.ndarray ] :

        """ Transforms a real or complex discrete-time incident signal to a
            real discrete-frequency reference signal.

            Arguments :
                x : Union[ List, numpy.ndarray ] - incident signal.
                b : Union[ List, numpy.ndarray ] - forward coefficient.
                index : int.
                spectrogram : bool.

            Returns :
                y : numpy.ndarray - reference signal.
                f : numpy.ndarray - frequency normalized to Nyquist in [ -1.0, 1.0 ).
        """

        if ( not isinstance( x, numpy.ndarray ) ) :
            x = numpy.array( list( x ) )
        if ( not len( x ) ) :
            raise ValueError( f'X = {x}' )
        if ( not isinstance( b, numpy.ndarray ) ) :    
            b = numpy.array( list( b ) )
        if ( ( not len( b ) ) or ( numpy.isclose( b, 0.0 ).all( ) ) ) :
            raise ValueError( f'B = {b}' )
        if ( len( x ) < len( b ) ) :
            raise ValueError( f'X = {x}' )
        y = [ ]
        f : numpy.ndarray = numpy.ndarray( ( 0 ) )
        jj = len( b ) // 2
        for ii in range( 0, len( x ) - len( b ) + 1, index ) :
            v, f = FourierTransform.transform( x[ ii : ii + len( b ) ], b )
            y.append( abs( v[ jj : ] ) ** 2 )
        y, f = numpy.stack( y ) if ( spectrogram ) else numpy.sum( y, axis = 0 ) / len( y ), f[ jj : ]
        return y, f  # type: ignore
