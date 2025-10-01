"""**Description**
    Initialize.

**License**
    `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_
    © 2018 - 2025 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

**Author**
    Larry Turner, Schneider Electric, AI Hub, 2018-03-22.
"""

# isort: skip_file

from diamondback.commons import Log, RestClient, Serial
from diamondback.filters import (
    FirFilter,
    IirFilter,
    ComplexBandpassFilter,
    ComplexExponentialFilter,
    ComplexFrequencyFilter,
    DerivativeFilter,
    GoertzelFilter,
    IntegralFilter,
    PidFilter,
    PolynomialRateFilter,
    PolyphaseRateFilter,
    RankFilter,
    WindowFilter,
)
from diamondback.models import DiversityModel, GaussianModel, GaussianMixtureModel
from diamondback.transforms import (
    ComplexTransform,
    FourierTransform,
    PsdTransform,
    WaveletTransform,
    ZTransform,
)
from importlib.metadata import version

__all__ = [
    "Log",
    "RestClient",
    "Serial",
    "FirFilter",
    "IirFilter",
    "ComplexBandpassFilter",
    "ComplexExponentialFilter",
    "ComplexFrequencyFilter",
    "DerivativeFilter",
    "GoertzelFilter",
    "IntegralFilter",
    "PidFilter",
    "PolynomialRateFilter",
    "PolyphaseRateFilter",
    "RankFilter",
    "WindowFilter",
    "DiversityModel",
    "GaussianModel",
    "GaussianMixtureModel",
    "ComplexTransform",
    "FourierTransform",
    "PsdTransform",
    "WaveletTransform",
    "ZTransform",
]

__version__ = version("diamondback")
