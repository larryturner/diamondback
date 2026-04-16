"""**Description**
    Test.

**Example**

    ::

        pytest --capture=no --verbose

**License**
    `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_
    © 2018 - 2026 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

**Author**
    Larry Turner, Schneider Electric, AI Hub, 2018-04-03.
"""

import numpy

from diamondback import ComplexExponentialFilter, WaveletTransform


class TestWaveletTransform(object):
    """Test WaveletTransform."""

    def test_init(self):
        """Test init."""

        count = 3
        h = numpy.array(
            [
                0.235233603892082,
                0.570558457915722,
                0.325182500263116,
                -0.095467207784164,
                -0.060416104155198,
                0.024908749868442,
            ]
        )
        g = numpy.array(
            [
                -0.024908749868442,
                -0.060416104155198,
                0.095467207784164,
                0.325182500263116,
                -0.570558457915722,
                0.235233603892082,
            ]
        )
        wavelet_transform = WaveletTransform("Daubechies", len(h) - 1)
        assert numpy.allclose(wavelet_transform.b[0][0], h)
        assert numpy.allclose(wavelet_transform.b[0][1], g)
        h = numpy.array(
            [
                0.024908749868442,
                -0.060416104155198,
                -0.095467207784164,
                0.325182500263116,
                0.570558457915722,
                0.235233603892082,
            ]
        )
        g = numpy.array(
            [
                0.235233603892082,
                -0.570558457915722,
                0.325182500263116,
                0.095467207784164,
                -0.060416104155198,
                -0.024908749868442,
            ]
        )
        assert numpy.allclose(wavelet_transform.b[1][0], h)
        assert numpy.allclose(wavelet_transform.b[1][1], g)
        h = numpy.array([0.5, 0.5])
        g = numpy.array([0.5, -0.5])
        wavelet_transform = WaveletTransform("Haar", len(h) - 1)
        assert numpy.allclose(wavelet_transform.b[0][0], h)
        assert numpy.allclose(wavelet_transform.b[0][1], g)
        h = numpy.array([0.5, 0.5])
        g = numpy.array([-0.5, 0.5])
        assert numpy.allclose(wavelet_transform.b[1][0], h)
        assert numpy.allclose(wavelet_transform.b[1][1], g)
        u = numpy.array(
            [
                -0.677118658500953,
                0.345009188833763,
                0.118882064536892,
                -0.537364409907213,
                -0.250663848240361,
                0.491955501906881,
                -0.545336874797487,
                0.390418096834100,
                -0.271946313073118,
                0.047745751406263,
                0.301454810260592,
                0.138563567406933,
                -0.215817816000671,
                -0.271946313073118,
                0.047745751406264,
                0.301454810260592,
                -0.154508497187474,
                -0.110615871041237,
                -0.024471741852423,
                0.071019760960103,
                0.139384128958763,
                0.154508497187474,
                0.110615871041237,
                0.024471741852423,
                -0.071019760960103,
                -0.139384128958763,
                -0.154508497187474,
                -0.110615871041237,
                -0.024471741852423,
                0.071019760960104,
                0.139384128958763,
                0.154508497187474,
            ]
        )
        x = ComplexExponentialFilter(0.5).filter(numpy.ones(len(u)) * 0.1).real
        y = wavelet_transform.transform(x, count, False)
        assert numpy.allclose(y, u)
        z = wavelet_transform.transform(y, count, True)
        assert numpy.allclose(z, x)
        x = numpy.zeros((len(u), len(u)))
        for ii in range(0, x.shape[0]):
            x[ii, :] = (
                numpy.random.rand()
                * ComplexExponentialFilter(numpy.random.rand() * 2.0 - 1.0)
                .filter(numpy.ones(len(u)) * numpy.random.rand() * 0.5)
                .real
            )
        z = wavelet_transform.transform(wavelet_transform.transform(x, count, False), count, True)
        assert numpy.allclose(z, x)
