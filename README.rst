diamondback
===========

.. image:: https://img.shields.io/pypi/pyversions/diamondback.svg?color=steelblue
    :target: https://www.python.org/
.. image:: https://img.shields.io/pypi/v/diamondback.svg?label=pypi&color=midnightblue
    :target: https://pypi.org/project/diamondback
.. image:: https://img.shields.io/badge/admin-nox-orangered
    :target: https://pypi.org/project/nox/
.. image:: https://img.shields.io/badge/doc-sphinx-royalblue
    :target: https://pypi.org/project/sphinx/
.. image:: https://img.shields.io/badge/test-pytest-forestgreen
    :target: https://pypi.org/project/pytest/
.. image:: https://img.shields.io/github/license/larryturner/diamondback?color=darkslategray
    :target: https://github.com/larryturner/diamondback/blob/master/LICENSE

Description
~~~~~~~~~~~

*diamondback* Digital Signal Processing (DSP).

*diamondback* complements Artificial Intelligence (AI) frameworks, by defining
components which filter, model, and transform data into forms which are
useful in feature extraction and pattern recognition.

*diamondback* supports applications including cancellation, identification,
optimization, probabilistic modeling, rate adaptation, and serialization.

Installation
~~~~~~~~~~~~

*diamondback* is a public repository hosted at `PyPi <https://pypi.org/project/diamondback>`_ and `GitHub <https://github.com/larryturner/diamondback>`_.

.. code-block:: bash

    pip install diamondback

.. code-block:: bash

    pip install git+https://github.com/larryturner/diamondback.git

.. code-block:: bash

    git clone https://github.com/larryturner/diamondback.git
    cd diamondback
    pip install .

Details
~~~~~~~

Data collections are consistently expressed in native types, including tuples, sets,
lists, and dictionaries, with vector and matrix types expressed in numpy arrays.
Complex or real types are supported as appropriate.

*diamondback* is defined in subpackages *commons*, *filters*, *models*, and
*transforms*.

`commons <https://larryturner.github.io/diamondback/diamondback.commons>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-   `Log <https://larryturner.github.io/diamondback/diamondback.commons#diamondback-commons-log-module>`_
    singleton instance which formats and writes log entries with a specified
    level and stream using the loguru package. Log entries contain an ISO-8601
    datetime and level.  Log uses lazy initialization to coexist with loguru.
    Dynamic stream redirection and level specification are supported.

-   `RestClient <https://larryturner.github.io/diamondback/diamondback.commons#diamondback-commons-rest-client-module>`_
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

-   `ComplexBandpassFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-complex-bandpass-filter-module>`_
    instances adaptively extract or reject signals at a normalized
    frequency of interest, and may be employed to dynamically track
    magnitude and phase or demodulate signals.

-   `ComplexExponentialFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-complex-exponential-filter-module>`_
    instances synthesize complex exponential signals at normalized
    frequencies of interest with contiguous phase.

-   `ComplexFrequencyFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-complex-frequency-filter-module>`_
    instances adaptively discriminate and estimate a normalized frequency
    of a signal.

-   `DerivativeFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-derivative-filter-module>`_
    instances estimate discrete derivative approximations at several
    filter orders.

-   `FirFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-fir-filter-module>`_
    instances realize discrete difference equations of Finite Impulse
    Response (FIR) form. Instances are defined based on style,
    normalized frequency, order, cascade count, and complement, or
    forward coefficients. Root extraction, group delay, and frequency
    response evaluation are defined.

-   `GoertzelFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-goertzel-filter-module>`_
    instances efficiently evaluate a Discrete Fourier Transform (DFT)
    at a normalized frequency, based on a window filter and normalized
    frequency.

-   `IirFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-iir-filter-module>`_
    instances realize discrete difference equations of Infinite Impulse
    Response (IIR) form. Instances are defined based on style,
    normalized frequency, order, cascade count, and complement, or recursive
    and forward coefficients. Root extraction, group delay, and frequency
    response evaluation are defined.

-   `IntegralFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-integral-filter-module>`_
    instances estimate discrete integral approximations at several filter
    orders.

-   `PidFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-pid-filter-module>`_
    instances realize discrete difference equations of Proportional
    Integral Derivative (PID) form.

-   `PolynomialRateFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-polynomial-rate-filter-module>`_
    instances approximate a signal evaluated at an effective frequency
    equal to the product of the normalized frequency and a rate greater
    than zero, supporting decimation and interpolation through localized
    polynomial approximation with no group delay.

-   `PolyphaseRateFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-polyphase-rate-filter-module>`_
    instances approximate a signal evaluated at an effective frequency
    equal to the product of the normalized frequency and a rate greater
    than zero, supporting decimation and interpolation through
    definition and application of a polyphase filter bank, a sequence
    of low pass filters with a common frequency response and a fractional
    sample difference in group delay. An appropriate stride is determined
    to realize the specified effective frequency without bias and with
    group delay based on order.

-   `RankFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-rank-filter-module>`_
    instances define nonlinear morphological operators, which define
    behavior based on rank and order, including dilation, median,
    and erosion, and may be combined in sequences to support close and
    open.

-   `WindowFilter <https://larryturner.github.io/diamondback/diamondback.filters#diamondback-filters-window-filter-module>`_
    instances realize discrete window functions useful in Fourier
    analysis, based on style, order, and normalization.

`models <https://larryturner.github.io/diamondback/diamondback.models>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-   `DiversityModel <https://larryturner.github.io/diamondback/diamondback.models#diamondback-models-diversity-model-module>`_
    instances select and retain a state extracted to maximize the minimum
    distance between state members based on style and order. An
    opportunistic unsupervised learning model typically improves condition
    and numerical accuracy and reduces storage relative to alternative
    approaches including generalized linear inverse.

-   `GaussianModel <https://larryturner.github.io/diamondback/diamondback.models#diamondback-models-gaussian-model-module>`_
    is a supervised learning probabilistic model instance which uses
    maximum likelihood estimation and regularization to maximize posterior
    probability and classify an incident signal.  Learns one distribution
    instance per class.

-   `GaussianMixtureModel <https://larryturner.github.io/diamondback/diamondback.models#diamondback-models-gaussian-mixture-model-module>`_
    is a semi-supervised learning probabilistic model instance which uses
    maximum likelihood estimation, regularization, and expectation
    maximization to maximize posterior probability and classify an incident
    signal.  Learns model instances of a specified order per class, where
    intra-class models capture mixture distributions.

`transforms <https://larryturner.github.io/diamondback/diamondback.transforms>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-   `ComplexTransform <https://larryturner.github.io/diamondback/diamondback.transforms#diamondback-transforms-complex-transform-module>`_
    is a singleton instance which converts a three-phase real signal to a
    complex signal, or a complex signal to a three-phase real signal, in
    equivalent and reversible representations, based on a neutral
    condition.

-   `FourierTransform <https://larryturner.github.io/diamondback/diamondback.transforms#diamondback-transforms-fourier-transform-module>`_
    is a singleton instance which converts a real or complex
    discrete-time signal to a complex discrete-frequency signal, or a
    complex discrete-frequency signal to a real or complex discrete-time
    signal, in equivalent and reversible representations, based on a
    window filter and inverse.

-   `PsdTransform <https://larryturner.github.io/diamondback/diamondback.transforms#diamondback-transforms-psd-transform-module>`_
    is a singleton instance which realizes a Power Spectral Density (PSD)
    which converts a real or complex discrete-time signal to a real
    discrete-frequency signal which estimates an aggregate power spectrum
    of the signal, based on a window filter, index, and spectrogram.
    A spectrogram constructs a time frequency representation of the power
    spectrum.

-   `WaveletTransform <https://larryturner.github.io/diamondback/diamondback.transforms#diamondback-transforms-wavelet-transform-module>`_
    instances realize a temporal spatial frequency transformation through
    defninition and application of analysis and synthesis filters with
    complementary frequency responses, combined with downsampling and
    upsampling operations, in equivalent and reversible representations.
    Instances are defined based on style and order.

-   `ZTransform <https://larryturner.github.io/diamondback/diamondback.transforms#diamondback-transforms-z-transform-module>`_
    is a singleton instance which converts continuous s-domain to
    discrete z-domain difference equations, based on a normalized
    frequency and application of bilinear or impulse invariant methods.

Dependencies
~~~~~~~~~~~~

*diamondback* depends upon external packages.

-   `jsonpickle <https://pypi.org/project/jsonpickle/>`_
-   `loguru <https://pypi.org/project/loguru/>`_
-   `numpy <https://pypi.org/project/numpy/>`_
-   `requests <https://pypi.org/project/requests/>`_
-   `scikit-learn <https://pypi.org/project/scikit-learn/>`_
-   `scipy <https://pypi.org/project/scipy/>`_

*diamondback* elective build, dependencies, docs, format, lint, notebook,
tests, and typing behavior depends upon additional external packages.

-   `build <https://pypi.org/project/build/>`_
-   `ipython <https://pypi.org/project/ipython/>`_
-   `ipywidgets <https://pypi.org/project/ipywidgets/>`_
-   `jupyter <https://pypi.org/project/jupyter/>`_
-   `matplotlib <https://pypi.org/project/matplotlib/>`_
-   `mypy <https://pypi.org/project/mypy/>`_
-   `nox <https://pypi.org/project/nox/>`_
-   `pandas <https://pypi.org/project/pandas/>`_
-   `pillow <https://pypi.org/project/pillow/>`_
-   `pydeps <https://pypi.org/project/pydeps/>`_
-   `pytest <https://pypi.org/project/pytest/>`_
-   `ruff <https://pypi.org/project/ruff/>`_
-   `sphinx <https://pypi.org/project/sphinx/>`_
-   `sphinx-rtd-theme <https://pypi.org/project/sphinx-rtd-theme/>`_

*diamondback* dependency diagram.

.. image:: https://larryturner.github.io/diamondback/dependencies-full.svg
    :target: https://larryturner.github.io/diamondback/dependencies-full.svg

Documentation
~~~~~~~~~~~~~

*diamondback* documentation is available on `GitHub Pages <https://larryturner.github.io/diamondback/>`_.

Run a nox *docs* session to generate documentation.

.. code-block:: bash

    nox -s docs

Notebook
~~~~~~~~

A jupyter notebook defines cells to create and exercise *diamondback* components.
The notebook serves as a tool for visualization, validation, and demonstration
of *diamondback* capabilities.

Run a nox *notebook* session to exercise notebook.  Restart kernel and run all cells,
then exercise widgets.

.. code-block:: bash

    nox -s notebook

Tests
~~~~~

A test solution is provided to exercise and verify components, pytest is
used to execute unit and integration tests.

Run a nox *tests* session to exercise tests.

.. code-block:: bash

    nox -s tests

License
~~~~~~~

`BSD-3-Clause <https://github.com/larryturner/diamondback/blob/master/LICENSE>`_

Author
~~~~~~

`Larry Turner <https://github.com/larryturner>`_
