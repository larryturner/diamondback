.. image:: https://img.shields.io/pypi/pyversions/diamondback.svg?color=blue
    :target: https://github.com/larryturner/diamondback
.. image:: https://img.shields.io/pypi/v/diamondback.svg?label=pypi%20version&color=lightblue
    :target: https://pypi.org/larryturner/diamondback
.. image:: https://img.shields.io/github/license/larryturner/diamondback?color=lightgray
    :target: https://github.com/larryturner/diamondback/blob/master/license

Description
~~~~~~~~~~~

Diamondback is a package which provides Digital Signal Processing ( DSP )
solutions, and complements AI frameworks, by defining components which filter,
model, and transform data.

Diamondback complements Artificial Intelligence ( AI ) frameworks, by
defining components which filter, model, and transform data into forms which
are useful in feature extraction and pattern recognition.

Diamondback also supports applications including cancellation, identification,
optimization, probabilistic modeling, rate adaptation, and serialization.

Details
~~~~~~~

Data collections are consistently expressed in native types,
including tuples, sets, lists, and dictionaries, with vector and matrix
types expressed in numpy arrays.  Complex or real types are supported as
appropriate.

Diamondback is defined in subpackages commons, filters, models, and
transforms.

`commons <https://larryturner.github.io/diamondback/diamondback.commons>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-   `Log <https://larryturner.github.io/diamondback/diamondback.commons#diamondback-commons-log-module>`_
    singleton instance which formats and writes log entries with a specified
    level and stream using the loguru package. Log entries contain an ISO-8601
    datetime and level.  Log uses lazy initialization to coexist with loguru.
    Dynamic stream redirection and level specification are supported.

-   `RestClient <https://larryturner.github.io/diamondback/diamondback.commons#diamondback-commons-restclient-module>`_
    instances define a client for simple REST service requests using the
    requests package.  An API and an elective dictionary of parameter strings
    are encoded to build a URL, elective binary or JSON data are defined in the
    body of a request, and a requests response containing JSON, text, or binary
    data is returned.  Proxy, timeout, and URL definition are supported.

-   `Serial <https://larryturner.github.io/diamondback/diamondback.commons#diamondback-commons-serial-module>`_
    singleton instance which encodes and decodes an instance or collection in
    BSON or JSON, and generates SHA3-256 codes, using the jsonpickle package.
    An instance may be an object or a collection, referenced by abstract or
    concrete types, and the instance will be correctly encoded and decoded,
    without custom encoding definitions.

`filters <https://larryturner.github.io/diamondback/diamondback.filters>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-   `ComplexBandPassFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-complexbandpassfilter-module>`_
    instances adaptively extract or reject signals at a normalized
    frequency of interest, and may be employed to dynamically track
    magnitude and phase or demodulate signals.

-   `ComplexExponentialFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-complexexponentialfilter-module>`_
    instances synthesize complex exponential signals at normalized
    frequencies of interest with contiguous phase.

-   `ComplexFrequencyFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-complexfrequencyfilter-module>`_
    instances adaptively discriminate and estimate a normalized frequency
    of a signal.

-   `DerivativeFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-derivativefilter-module>`_
    instances estimate discrete derivative approximations at several
    filter orders.

-   `FirFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-firfilter-module>`_
    instances realize discrete difference equations of Finite Impulse
    Response ( FIR ) form. Instances are defined based on style,
    normalized frequency, order, cascade count, and complement, or
    forward coefficients. Root extraction, group delay, and frequency
    response evaluation are defined.

-   `GoertzelFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-goertzelfilter-module>`_
    instances efficiently evaluate a Discrete Fourier Transform ( DFT )
    at a normalized frequency, based on a window filter and normalized
    frequency.

-   `IirFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-iirfilter-module>`_
    instances realize discrete difference equations of Infinite Impulse
    Response ( IIR ) form. Instances are defined based on style,
    normalized frequency, order, cascade count, and complement, or recursive
    and forward coefficients. Root extraction, group delay, and frequency
    response evaluation are defined.

-   `IntegralFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-integralfilter-module>`_
    instances estimate discrete integral approximations at several filter
    orders.

-   `PidFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-pidfilter-module>`_
    instances realize discrete difference equations of Proportional
    Integral Derivative ( PID ) form.

-   `PolynomialRateFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-polynomialratefilter-module>`_
    instances approximate a signal evaluated at an effective frequency
    equal to the product of the normalized frequency and a rate greater
    than zero, supporting decimation and interpolation through localized
    polynomial approximation with no group delay.

-   `PolyphaseRateFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-polyphaseratefilter-module>`_
    instances approximate a signal evaluated at an effective frequency
    equal to the product of the normalized frequency and a rate greater
    than zero, supporting decimation and interpolation through
    definition and application of a polyphase filter bank, a sequence
    of low pass filters with a common frequency response and a fractional
    sample difference in group delay. An appropriate stride is determined
    to realize the specified effective frequency without bias and with
    group delay based on order.

-   `RankFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-rankfilter-module>`_
    instances define nonlinear morphological operators, which define
    functionality based on rank and order, including dilation, median,
    and erosion, and may be combined in sequences to support close and
    open.

-   `WindowFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-windowfilter-module>`_
    instances realize discrete window functions useful in Fourier
    analysis, based on style, order, and normalization.

`models <https://larryturner.github.io/diamondback/diamondback.models>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-   `DiversityModel <https://larryturner.github.io/diamondback/diamondback.models#diamondback-models-diversitymodel-module>`_
    instances select and retain a state extracted to maximize the minimum
    distance between state members based on style and order. An
    opportunistic unsupervised learning model typically improves condition
    and numerical accuracy and reduces storage relative to alternative
    approaches including generalized linear inverse.

-   `GaussianModel <https://larryturner.github.io/diamondback/diamondback.models#diamondback-models-gaussianmodel-module>`_
    is a supervised learning probabilistic model instance which uses
    maximum likelihood estimation and regularization to maximize posterior
    probability and classify an incident signal.  Learns one distribution
    instance per class.

-   `GaussianMixtureModel <https://larryturner.github.io/diamondback/diamondback.models#diamondback-models-gaussianmixturemodel-module>`_
    is a semi-supervised learning probabilistic model instance which uses
    maximum likelihood estimation, regularization, and expectation
    maximization to maximize posterior probability and classify an incident
    signal.  Learns model instances of a specified order per class, where
    intra-class models capture mixture distributions. 

`transforms <https://larryturner.github.io/diamondback/diamondback.transforms>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-   `ComplexTransform <https://larryturner.github.io/diamondback/diamondback.transforms#diamondback-transforms-complextransform-module>`_
    is a singleton instance which converts a three-phase real signal to a
    complex signal, or a complex signal to a three-phase real signal, in
    equivalent and reversible representations, based on a neutral
    condition.

-   `FourierTransform <https://larryturner.github.io/diamondback/diamondback.transforms#diamondback-transforms-fouriertransform-module>`_
    is a singleton instance which converts a real or complex
    discrete-time signal to a complex discrete-frequency signal, or a
    complex discrete-frequency signal to a real or complex discrete-time
    signal, in equivalent and reversible representations, based on a
    window filter and inverse.

-   `PowerSpectrumTransform <https://larryturner.github.io/diamondback/diamondback.transforms#diamondback-transforms-powerspectrumtransform-module>`_
    is a singleton instance which converts a real or complex
    discrete-time signal to a real discrete-frequency signal which
    estimates a mean power density of the signal, based on a window
    filter.

-   `WaveletTransform <https://larryturner.github.io/diamondback/diamondback.transforms#diamondback-transforms-wavelettransform-module>`_
    instances realize a temporal spatial frequency transformation through
    defninition and application of analysis and synthesis filters with
    complementary frequency responses, combined with downsampling and
    upsampling operations, in equivalent and reversible representations.
    Instances are defined based on style and order.

-   `ZTransform <https://larryturner.github.io/diamondback/diamondback.transforms#diamondback-transforms-ztransform-module>`_
    is a singleton instance which converts continuous s-domain to
    discrete z-domain difference equations, based on a normalized
    frequency and application of bilinear or impulse invariant methods.

Dependencies
~~~~~~~~~~~~

Diamondback depends upon external packages :

-   `jsonpickle <https://github.com/jsonpickle/jsonpickle>`_

-   `loguru <https://github.com/delgan/loguru>`_

-   `numpy <https://github.com/numpy/numpy>`_

-   `pandas <https://github.com/pandas-dev/pandas>`_

-   `requests <https://github.com/psf/requests>`_

-   `scikit-learn <https://github.com/scikit-learn/scikit-learn>`_

-   `scipy <https://github.com/scipy/scipy>`_

Diamondback elective documentation, test, and visualization functionality
depends upon additional external packages :

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

    or

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
used to execute unit and integration tests.

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