.. image:: https://img.shields.io/pypi/pyversions/diamondback.svg?color=blue
    :target: https://github.com/larryturner/diamondback
.. image:: https://img.shields.io/pypi/v/diamondback.svg?label=pypi%20version&color=lightblue
    :target: https://pypi.org/larryturner/diamondback
.. image:: https://img.shields.io/github/license/larryturner/diamondback?color=lightgray
    :target: https://github.com/larryturner/diamondback/blob/master/license

Description
~~~~~~~~~~~

Diamondback is a package which provides Digital Signal Processing ( DSP )
solutions, organized in the form of commons, filters, interfaces, models,
and transforms.

Diamondback complements Artificial Intelligence ( AI ) frameworks, by
defining components which filter, model, and transform data into forms which
are useful in pattern recognition and feature extraction.

Diamondback also supports applications including compression, cancellation,
identification, modulation, differentiation, integration, rate adaptation,
clustering, and serialization.

Details
~~~~~~~

An extensible factory design pattern is expressed in many components,
and a mix-in design pattern is extensively employed in property
definition. Complex or real types, in adaptive or static forms, are
supported as appropriate. Data collections are consistently expressed in
native types, including tuples, sets, lists, and dictionaries, with
vector and matrix types expressed in numpy arrays.

Diamondback is defined in subpackages :

-   `commons <https://larryturner.github.io/diamondback/diamondback.commons>`_

-   `filters <https://larryturner.github.io/diamondback/diamondback.filters>`_

-   `interfaces <https://larryturner.github.io/diamondback/diamondback.interfaces>`_

-   `models <https://larryturner.github.io/diamondback/diamondback.models>`_

-   `transforms <https://larryturner.github.io/diamondback/diamondback.transforms>`_

`commons <https://larryturner.github.io/diamondback/diamondback.commons>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-   `Log <https://larryturner.github.io/diamondback/diamondback.commons#module-diamondback.commons.Log>`_
    singleton instance which formats and writes log entries with a specified
    level and stream using the loguru package. Log entries contain an ISO-8601
    datetime and level.  Log uses lazy initialization to coexist with loguru.
    Dynamic stream redirection and level specification are supported.

-   `RestClient <https://larryturner.github.io/diamondback/diamondback.commons#module-diamondback.commons.RestClient>`_
    instances define a client for simple REST service requests using the
    requests package.  An API and an elective dictionary of parameter strings
    are encoded to build a URL, elective binary or JSON data are defined in the
    body of a request, and a requests response containing JSON, text, or binary
    data is returned.  Proxy, timeout, and URL definition are supported.

-   `Serial <https://larryturner.github.io/diamondback/diamondback.commons#module-diamondback.commons.Serial>`_
    singleton instance which encodes and decodes an instance or collection in
    BSON or JSON, and generates SHA3-256 codes, using the jsonpickle package.
    An instance may be an object or a collection, referenced by abstract or
    concrete types, and the instance will be correctly encoded and decoded,
    without custom encoding definitions.

`filters <https://larryturner.github.io/diamondback/diamondback.filters>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-   `ComplexBandPassFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.ComplexBandPassFilter>`_
    instances adaptively extract or reject signals at a normalized
    frequency of interest, and may be employed to dynamically track
    magnitude and phase or demodulate signals.

-   `ComplexExponentialFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.ComplexExponentialFilter>`_
    instances synthesize complex exponential signals at normalized
    frequencies of interest with contiguous phase.

-   `ComplexFrequencyFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.ComplexFrequencyFilter>`_
    instances adaptively discriminate and estimate a normalized frequency
    of a signal.

-   `DerivativeFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.DerivativeFilter>`_
    instances estimate discrete derivative approximations at several
    filter orders, through extensible factory construction.

-   `FirFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.FirFilter>`_
    instances realize discrete difference equations of Finite Impulse
    Response ( FIR ) form. A factory electively constructs instances based
    on type, classification, normalized frequency, order, cascade count, and
    complement. Filters may be readily extended to support new types and
    functionality, while retaining factory support. Root extraction, group
    delay, and frequency response evaluation are defined.

-   `GoertzelFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.GoertzelFilter>`_
    instances efficiently evaluate a Discrete Fourier Transform ( DFT )
    at a normalized frequency, based on a window filter and normalized
    frequency.

-   `IirFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.IirFilter>`_
    instances realize discrete difference equations of Infinite Impulse
    Response ( IIR ) form. A factory electively constructs instances based
    on type, classification, normalized frequency, order, cascade count, and
    complement. Filters may be readily extended to support new types and
    functionality, while retaining factory support. Root extraction, group
    delay, and frequency response evaluation are defined.

-   `IntegralFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.IntegralFilter>`_
    instances estimate discrete integral approximations at several filter
    orders, through extensible factory construction.

-   `PidFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.PidFilter>`_
    instances realize discrete difference equations of Proportional
    Integral Derivative ( PID ) form.

-   `PolynomialRateFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.PolynomialRateFilter>`_
    instances approximate a signal evaluated at an effective frequency
    equal to the product of the normalized frequency and a rate greater
    than zero, supporting decimation and interpolation through localized
    polynomial approximation with no group delay.

-   `PolyphaseRateFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.PolyphaseRateFilter>`_
    instances approximate a signal evaluated at an effective frequency
    equal to the product of the normalized frequency and a rate greater
    than zero, supporting decimation and interpolation through
    construction and application of a polyphase filter bank, a sequence
    of low pass filters with a common frequency response and a fractional
    sample difference in group delay. An appropriate stride is determined
    to realize the specified effective frequency without bias and with
    group delay based on order.

-   `RankFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.RankFilter>`_
    instances define nonlinear morphological operators, which define
    functionality based on rank and order, including dilation, median,
    and erosion, and may be combined in sequences to support close and
    open.

-   `WindowFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.WindowFilter>`_
    instances realize discrete window functions useful in Fourier
    analysis, based on type, classification, order, and normalization,
    through extensible factory construction.

`interfaces <https://larryturner.github.io/diamondback/diamondback.interfaces>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-   `IA <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IA>`_,
    `IB <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IB>`_,
    `IClear <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IClear>`_,
    `IConfigure <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IConfigure>`_,
    `ICount <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.ICount>`_,
    `IData <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IData>`_,
    `IDate <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IDate>`_,
    `IDispose <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IDispose>`_,
    `IDuration <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IDuration>`_,
    `IEqual <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IEqual>`_,
    `IFrequency <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IFrequency>`_,
    `IIdentity <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IIdentity>`_,
    `IInterval <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IInterval>`_,
    `ILabel <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.ILabel>`_,
    `ILatency <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.ILatency>`_,
    `ILive <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.ILive>`_,
    `IModel <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IModel>`_,
    `IPath <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IPath>`_,
    `IPeriod <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IPeriod>`_,
    `IPhase <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IPhase>`_,
    `IProxy <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IProxy>`_,
    `IQ <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IQ>`_,
    `IRate <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IRate>`_,
    `IReady <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IReady>`_,
    `IReset <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IReset>`_,
    `IResolution <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IResolution>`_,
    `IRotation <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IRotation>`_,
    `IS <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IS>`_,
    `IStream <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IStream>`_,
    `ITimeOut <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.ITimeOut>`_,
    `ITimeZone <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.ITimeZone>`_,
    `IUrl <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IUrl>`_,
    `IValid <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IValid>`_,
    and
    `IVersion <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IVersion>`_,
    interfaces facilitate mix-in design.

`models <https://larryturner.github.io/diamondback/diamondback.models>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-   `DiversityModel <https://larryturner.github.io/diamondback/diamondback.models#module-diamondback.models.DiversityModel>`_
    instances select and retain a state extracted to maximize the minimum
    distance between state members based on classification and order,
    through extensible factory construction. An opportunistic
    unsupervised learning model typically improves condition and
    numerical accuracy and reduces storage relative to alternative
    approaches including generalized linear inverse.

-   `PrincipalComponentModel <https://larryturner.github.io/diamondback/diamondback.models#module-diamondback.models.PrincipalComponentModel>`_
    instances are supervised learning models which analyze an incident
    signal to learn a mean vector, standard deviation vector, and a
    collection of eigenvectors, and produce a reference signal which is a
    candidate for dimension reduction, in which higher order dimensions
    are discarded, reducing the order of the reference signal, while
    preserving significant and often sufficient information.

`transforms <https://larryturner.github.io/diamondback/diamondback.transforms>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-   `ComplexTransform <https://larryturner.github.io/diamondback/diamondback.transforms#module-diamondback.transforms.ComplexTransform>`_
    is a singleton instance which converts a three-phase real signal to a
    complex signal, or a complex signal to a three-phase real signal, in
    equivalent and reversible representations, based on a neutral
    condition.

-   `FourierTransform <https://larryturner.github.io/diamondback/diamondback.transforms#module-diamondback.transforms.FourierTransform>`_
    is a singleton instance which converts a real or complex
    discrete-time signal to a complex discrete-frequency signal, or a
    complex discrete-frequency signal to a real or complex discrete-time
    signal, in equivalent and reversible representations, based on a
    window filter and inverse.

-   `PowerSpectrumTransform <https://larryturner.github.io/diamondback/diamondback.transforms#module-diamondback.transforms.PowerSpectrumTransform>`_
    is a singleton instance which converts a real or complex
    discrete-time signal to a real discrete-frequency signal which
    estimates a mean power density of the signal, based on a window
    filter.

-   `WaveletTransform <https://larryturner.github.io/diamondback/diamondback.transforms#module-diamondback.transforms.WaveletTransform>`_
    instances realize a temporal spatial frequency transformation through
    construction and application of analysis and synthesis filters with
    complementary frequency responses, combined with downsampling and
    upsampling operations, in equivalent and reversible representations.
    A factory constructs instances based on type, classification, and
    order. Filters may be readily extended to support new types and
    functionality, while retaining factory support.

-   `ZTransform <https://larryturner.github.io/diamondback/diamondback.transforms#module-diamondback.transforms.ZTransform>`_
    is a singleton instance which converts continuous s-domain to
    discrete z-domain difference equations, based on a normalized
    frequency and application of bilinear or impulse invariant methods.

Dependencies
~~~~~~~~~~~~

Diamondback depends upon external packages :

::

    pip install diamondback

-   `jsonpickle <https://github.com/jsonpickle/jsonpickle>`_

-   `loguru <https://github.com/delgan/loguru>`_

-   `numpy <https://github.com/numpy/numpy>`_

-   `pandas <https://github.com/pandas-dev/pandas>`_

-   `requests <https://github.com/psf/requests>`_

-   `scipy <https://github.com/scipy/scipy>`_

Diamondback elective documentation, test, and visualization functionality
depends upon additional external packages :

::

    pip install diamondback[ full ]

    or

    pip install --requirement requirements.txt

-   `ipython <https://github.com/ipython/ipython>`_

-   `ipywidgets <https://github.com/jupyter-widgets/ipywidgets>`_

-   `jupyter <https://github.com/jupyter/notebook>`_

-   `matplotlib <https://github.com/matplotlib/matplotlib>`_

-   `nox <https://github.com/theacodes/nox>`_

-   `pillow <https://github.com/python-pillow/pillow>`_

-   `pytest <https://github.com/pytest-dev/pytest>`_

-   `sphinx <https://github.com/sphinx-doc/sphinx>`_

-   `sphinx-rtd-theme <https://github.com/readthedocs/sphinx_rtd_theme>`_

Installation
~~~~~~~~~~~~

Diamondback is a public repository hosted at PyPI and GitHub.

::

    pip install diamondback

    pip install git+https://github.com/larryturner/diamondback.git

Demonstration
~~~~~~~~~~~~~

A jupyter notebook defines cells to create and exercise diamondback components.
The notebook serves as a tool for visualization, validation, and demonstration
of diamondback capabilities.

A jupyter notebook may be run on a remote server without installation with
Binder, which dynamically builds and deploys a docker container from a GitHub
repository, or installed from GitHub and run on a local system.

**Remote**

.. image:: https://img.shields.io/badge/binder-blue
    :target: https://mybinder.org/v2/gh/larryturner/diamondback/master?filepath=jupyter%2Fdiamondback.ipynb

**Local**

::

    git clone https://github.com/larryturner/diamondback.git

    cd diamondback

    pip install --requirement requirements.txt

    jupyter notebook .\jupyter\diamondback.ipynb

Restart the kernel, as the first cell contains common definitions, find cells
which exercise components of interest, and manipulate widgets to exercise and
visualize functionality.

Tests
~~~~~

A test solution is provided to exercise and verify components, pytest is
used to execute unit and scenario tests.

::

    pytest --capture=no --verbose

Documentation
~~~~~~~~~~~~~

Diamondback documentation is generated from the source, indexed, and searchable
from GitHub pages.

.. image:: https://img.shields.io/badge/github-blue
    :target: https://larryturner.github.io/diamondback/index.html

License
~~~~~~~

`BSD-3C <https://github.com/larryturner/diamondback/blob/master/license>`_

Author
~~~~~~

`Larry Turner <https://github.com/larryturner>`_
