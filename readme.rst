Description
~~~~~~~~~~~

Diamondback is a Python package which provides Digital Signal Processing
( DSP ) solutions, organized in the form of commons, filters,
interfaces, models, and transforms.

Diamondback was designed to complement Artificial Intelligence ( AI )
frameworks, by defining components which analyze, filter, extract,
model, and transform data into forms which are useful in applications
including pattern recognition, feature extraction, and optimization.

Diamondback was also designed to provide utility in the context of
classical signal processing solutions including communications,
modeling, signal identification and extraction, and noise cancellation.

Documentation is provided in HTML form, extracted from docstrings in the
diamondback package source, and a jupyter notebook is provided to
dynamically construct and exercise diamondback components to facilitate
experimentation and visualization.

Details
~~~~~~~

An extensible factory design pattern is expressed in many components,
and a mix-in design pattern is extensively employed in property
definition. Complex or real types, in adaptive or static forms, are
supported as appropriate. Data collections are consistently expressed in
native types, including tuples, sets, lists, and dictionaries, with
vector and matrix types expressed in numpy arrays.

Diamondback is defined in subpackages :

-  `clients <https://larryturner.github.io/diamondback/diamondback.clients>`__

-  `commons <https://larryturner.github.io/diamondback/diamondback.commons>`__

-  `filters <https://larryturner.github.io/diamondback/diamondback.filters>`__

-  `interfaces <https://larryturner.github.io/diamondback/diamondback.interfaces>`__

-  `models <https://larryturner.github.io/diamondback/diamondback.models>`__

-  `transforms <https://larryturner.github.io/diamondback/diamondback.transforms>`__

`clients <https://larryturner.github.io/diamondback/diamondback.clients>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  `RestClient <https://larryturner.github.io/diamondback/diamondback.clients#module-diamondback.clients.RestClient>`__
   instances define a client for simple REST service requests.  An API and an
   elective dictionary of parameter strings are encoded to build a URL,
   elective JSON or binary data are defined in the body of a request, and a
   JSON, binary, or text response is returned and decoded.  A client instance
   may be useful as a base client definition to interact with a service which
   satisfies flexible request constraints. Caching may be useful in
   environments with intermittent or inconsistent network connectivity.  If
   caching is specified, requests are cached when a service is not live, and
   sent in order during a subsequent request when a service is live.

`commons <https://larryturner.github.io/diamondback/diamondback.commons>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  `Log <https://larryturner.github.io/diamondback/diamondback.commons#module-diamondback.commons.Log>`__
   singleton instance which formats and writes log entries, electively
   using the logger package or directly to a specified stream. Log
   entries are prefaced with an ISO-8601 datetime and log level, and
   enhancements are made to the formatting of datetime, exception, and
   collection data types. Dynamic stream redirection and log level
   specification are supported.

-  `Serial <https://larryturner.github.io/diamondback/diamondback.commons#module-diamondback.commons.Serial>`__
   singleton instance which encodes and decodes an instance or
   collection with JSON, or base-64 encoded gzip JSON binary format.

`filters <https://larryturner.github.io/diamondback/diamondback.filters>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  `ComplexBandPassFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.ComplexBandPassFilter>`__
   instances adaptively extract or reject signals at a normalized
   frequency of interest, and may be employed to dynamically track
   magnitude and phase or demodulate signals.

-  `ComplexExponentialFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.ComplexExponentialFilter>`__
   instances synthesize complex exponential signals at normalized
   frequencies of interest with contiguous phase.

-  `ComplexFrequencyFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.ComplexFrequencyFilter>`__
   instances adaptively discriminate and estimate a normalized frequency
   of a signal.

-  `DerivativeFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.DerivativeFilter>`__
   instances estimate discrete derivative approximations at several
   filter orders, through extensible factory construction.

-  `FirFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.FirFilter>`__
   instances realize discrete difference equations of Finite Impulse
   Response ( FIR ) form, in adaptive or static solutions. A factory
   electively constructs instances based on type, classification,
   normalized frequency, order, cascade count, and complement. Filters
   may be readily extended to support new types and functionality, while
   retaining factory support. Root extraction, group delay, and
   frequency response evaluation are defined.

-  `GoertzelFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.GoertzelFilter>`__
   instances efficiently evaluate a Discrete Fourier Transform ( DFT )
   at a normalized frequency, based on a window filter and normalized
   frequency.

-  `IirFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.IirFilter>`__
   instances realize discrete difference equations of Infinite Impulse
   Response ( IIR ) form, in adaptive or static solutions. A factory
   electively constructs instances based on type, classification,
   normalized frequency, order, cascade count, and complement. Filters
   may be readily extended to support new types and functionality, while
   retaining factory support. Root extraction, group delay, and
   frequency response evaluation are defined.

-  `IntegralFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.IntegralFilter>`__
   instances estimate discrete integral approximations at several filter
   orders, through extensible factory construction.

-  `PidFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.PidFilter>`__
   instances realize discrete difference equations of Proportional
   Integral Derivative ( PID ) form.

-  `PolynomialRateFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.PolynomialRateFilter>`__
   instances approximate a signal evaluated at an effective frequency
   equal to the product of the normalized frequency and a rate greater
   than zero, supporting decimation and interpolation through localized
   polynomial approximation with no group delay.

-  `PolyphaseRateFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.PolyphaseRateFilter>`__
   instances approximate a signal evaluated at an effective frequency
   equal to the product of the normalized frequency and a rate greater
   than zero, supporting decimation and interpolation through
   construction and application of a polyphase filter bank, a sequence
   of low pass filters with a common frequency response and a fractional
   sample difference in group delay. An appropriate stride is determined
   to realize the specified effective frequency without bias and with
   group delay based on order.

-  `RankFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.RankFilter>`__
   instances define nonlinear morphological operators, which define
   functionality based on rank and order, including dilation, median,
   and erosion, and may be combined in sequences to support close and
   open.

-  `WindowFilter <https://larryturner.github.io/diamondback/diamondback.filters#module-diamondback.filters.WindowFilter>`__
   instances realize discrete window functions useful in Fourier
   analysis, based on type, classification, order, and normalization,
   through extensible factory construction.

`interfaces <https://larryturner.github.io/diamondback/diamondback.interfaces>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  `IA <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IA>`__,
   `IAsset <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IAsset>`__,
   `IB <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IB>`__,
   `ICache <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.ICache>`__,
   `IClear <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IClear>`__,
   `ICompress <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.ICompress>`__,
   `IConfigure <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IConfigure>`__,
   `IConnect <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IConnect>`__,
   `ICount <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.ICount>`__,
   `IData <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IData>`__,
   `IDate <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IDate>`__,
   `IDispose <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IDispose>`__,
   `IDuration <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IDuration>`__,
   `IEmulate <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IEmulate>`__,
   `IEncoding <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IEncoding>`__,
   `IEqual <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IEqual>`__,
   `IFrequency <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IFrequency>`__,
   `IIdentity <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IIdentity>`__,
   `IInterval <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IInterval>`__,
   `ILatency <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.ILatency>`__,
   `ILive <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.ILive>`__,
   `IModel <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IModel>`__,
   `IPath <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IPath>`__,
   `IPeriod <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IPeriod>`__,
   `IPhase <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IPhase>`__,
   `IProxy <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IProxy>`__,
   `IQ <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IQ>`__,
   `IRate <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IRate>`__,
   `IReady <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IReady>`__,
   `IReset <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IReset>`__,
   `IResolution <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IResolution>`__,
   `IRotation <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IRotation>`__,
   `IS <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IS>`__,
   `IStream <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IStream>`__,
   `ITimeOut <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.ITimeOut>`__,
   `ITimeZone <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.ITimeZone>`__,
   `IUpdate <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IUpdate>`__,
   `IUrl <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IUrl>`__,
   `IUser <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IUser>`__,
   `IValid <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IValid>`__,
   `IVersion <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IVersion>`__,
   and
   `IWrite <https://larryturner.github.io/diamondback/diamondback.interfaces#module-diamondback.interfaces.IWrite>`__
   interfaces facilitate mix-in design.

`models <https://larryturner.github.io/diamondback/diamondback.models>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  `DiversityModel <https://larryturner.github.io/diamondback/diamondback.models#module-diamondback.models.DiversityModel>`__
   instances select and retain a state extracted to maximize the minimum
   distance between state members based on classification and order,
   through extensible factory construction. An opportunistic
   unsupervised learning model typically improves condition and
   numerical accuracy and reduces storage relative to alternative
   approaches including generalized linear inverse.

-  `PrincipalComponentModel <https://larryturner.github.io/diamondback/diamondback.models#module-diamondback.models.PrincipalComponentModel>`__
   instances are supervised learning models which analyze an incident
   signal to learn a mean vector, standard deviation vector, and a
   collection of eigenvectors, and produce a reference signal which is a
   candidate for dimension reduction, in which higher order dimensions
   are discarded, reducing the order of the reference signal, while
   preserving significant and often sufficient information.

`transforms <https://larryturner.github.io/diamondback/diamondback.transforms>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  `ComplexTransform <https://larryturner.github.io/diamondback/diamondback.transforms#module-diamondback.transforms.ComplexTransform>`__
   is a singleton instance which converts a three-phase real signal to a
   complex signal, or a complex signal to a three-phase real signal, in
   equivalent and reversible representations, based on a neutral
   condition.

-  `FourierTransform <https://larryturner.github.io/diamondback/diamondback.transforms#module-diamondback.transforms.FourierTransform>`__
   is a singleton instance which converts a real or complex
   discrete-time signal to a complex discrete-frequency signal, or a
   complex discrete-frequency signal to a real or complex discrete-time
   signal, in equivalent and reversible representations, based on a
   window filter and inverse.

-  `PowerSpectrumTransform <https://larryturner.github.io/diamondback/diamondback.transforms#module-diamondback.transforms.PowerSpectrumTransform>`__
   is a singleton instance which converts a real or complex
   discrete-time signal to a real discrete-frequency signal which
   estimates a mean power density of the signal, based on a window
   filter.

-  `WaveletTransform <https://larryturner.github.io/diamondback/diamondback.transforms#module-diamondback.transforms.WaveletTransform>`__
   instances realize a temporal spatial frequency transformation through
   construction and application of analysis and synthesis filters with
   complementary frequency responses, combined with downsampling and
   upsampling operations, in equivalent and reversible representations.
   A factory constructs instances based on type, classification, and
   order. Filters may be readily extended to support new types and
   functionality, while retaining factory support.

-  `ZTransform <https://larryturner.github.io/diamondback/diamondback.transforms#module-diamondback.transforms.ZTransform>`__
   is a singleton instance which converts continuous s-domain to
   discrete z-domain difference equations, based on a normalized
   frequency and application of bilinear or impulse invariant methods.

Dependencies
~~~~~~~~~~~~

Diamondback depends upon external packages :

-  `dateutil <https://github.com/dateutil/dateutil>`__

-  `jsonpickle <https://github.com/jsonpickle/jsonpickle>`__

-  `numpy <https://github.com/numpy/numpy>`__

-  `pandas <https://github.com/pandas-dev/pandas>`__

-  `scipy <https://github.com/scipy/scipy>`__

Diamondback jupyter notebook depends upon additional external packages :

-  `ipython <https://github.com/ipython/ipython>`__

-  `ipywidgets <https://github.com/jupyter-widgets/ipywidgets>`__

-  `jupyter <https://github.com/jupyter/notebook>`__

-  `matplotlib <https://github.com/matplotlib/matplotlib>`__

-  `pillow <https://github.com/python-pillow/pillow>`__

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

|Binder|

**Local**

::

    git clone https://github.com/larryturner/diamondback.git

    cd diamondback

    pip install --requirement requirements.txt

    jupyter notebook .\jupyter\diamondback.ipynb

Restart the kernel, as the first cell contains common definitions, find cells
which exercise components of interest, and manipulate widgets to exercise and
visualize functionality.

Documentation
~~~~~~~~~~~~~

Diamondback documentation is generated from the source, indexed, and searchable
from GitHub.

|GitHub|

Tests
~~~~~

A simple pytest solution is provided to exercise and verify diamondback
components.

::

    pytest --capture=no --verbose

Author
~~~~~~

`Larry Turner <https://github.com/larryturner>`__

License
~~~~~~~

`BSD-3C <https://github.com/larryturner/diamondback/blob/master/license>`__

Release
~~~~~~~

`Version <https://github.com/larryturner/diamondback/blob/master/version>`__

Copyright (c) 2018, Larry Turner, Schneider Electric. All rights reserved.

.. |Binder| image:: ./images/binder.png
   :target: https://mybinder.org/v2/gh/larryturner/diamondback/master?filepath=jupyter%2Fdiamondback.ipynb
.. |GitHub| image:: ./images/github.png
   :target: https://larryturner.github.io/diamondback/
