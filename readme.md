### Description

Diamondback is a Python package which provides Digital Signal Processing ( DSP )
solutions, organized in the form of commons, filters, interfaces, models, and
transforms.

Diamondback was designed to complement Artificial Intelligence ( AI ) frameworks,
by defining components which analyze, filter, extract, model, and transform data
into forms which are useful in applications including pattern recognition,
feature extraction, and optimization.

Diamondback was also designed to provide utility in the context of classical
signal processing solutions including communications, modeling, signal
identification and extraction, and noise cancellation.

Documentation is provided in HTML form, extracted from docstrings in the
diamondback package source, and a Jupyter notebook is provided to dynamically
construct and exercise diamondback components to facilitate experimentation and
visualization.
	
### Details

An extensible factory design pattern is expressed in many components, and a
mix-in design pattern is extensively employed in property definition.  Complex
or real types, in adaptive or static forms, are supported as appropriate.  Data
collections are consistently expressed in native types, including tuples, sets,
lists, and dictionaries, with vector and matrix types expressed in numpy arrays.
	
Diamondback is defined in subpackages :

* [commons](https://larryturner.github.io/diamondback/diamondback.commons)
	
* [filters](https://larryturner.github.io/diamondback/diamondback.filters)
	
* [interfaces](https://larryturner.github.io/diamondback/diamondback.interfaces)
	
* [models](https://larryturner.github.io/diamondback/diamondback.models)
	
* [transforms](https://larryturner.github.io/diamondback/diamondback.transforms)

#### [commons](https://larryturner.github.io/diamondback/diamondback.commons)
	
**Log** is a singleton instance which formats and writes log entries,
electively using the logger package or directly to a specified stream. Log
entries are prefaced with an ISO-8601 datetime and log level, and enhancements
are made to the formatting of datetime, exception, and collection data types.
Dynamic stream redirection and log level specification are supported.
	    
**Serial** is a singleton instance which encodes and decodes an instance or
collection with JSON text, or base-64 encoded gzip JSON binary format.

#### [filters](https://larryturner.github.io/diamondback/diamondback.filters)
	
**ComplexBandPassFilter** instances adaptively extract or reject signals at a
normalized frequency of interest, and may be employed to dynamically track
magnitude and phase or demodulate signals.
	
**ComplexExponentialFilter** instances synthesize complex exponential signals at
normalized frequencies of interest with contiguous phase.
	
**ComplexFrequencyFilter** instances adaptively discriminate and estimate a
normalized frequency of a signal.
	
**DerivativeFilter** instances estimate discrete derivative approximations at
several filter orders, through extensible factory construction.

**FirFilter** instances realize discrete difference equations of Finite Impulse
Response ( FIR ) form, in adaptive or static solutions.  A factory electively
constructs instances based on type, classification, normalized frequency, order,
cascade count, and complement.  Filters may be readily extended to support new
types and functionality, while retaining factory support.  Root extraction,
group delay, and frequency response evaluation are defined.

**GoertzelFilter** instances efficiently evaluate a Discrete Fourier Transform
( DFT ) at a normalized frequency, based on a window filter and normalized
frequency.
	
**IirFilter** instances realize discrete difference equations of Infinite Impulse
Response ( IIR ) form, in adaptive or static solutions.  A factory electively
constructs instances based on type, classification, normalized frequency, order,
cascade count, and complement.  Filters may be readily extended to support new
types and functionality, while retaining factory support.  Root extraction,
group delay, and frequency response evaluation are defined.

**IntegralFilter** instances estimate discrete integral approximations at several
filter orders, through extensible factory construction.

**PidFilter** instances realize discrete difference equations of Proportional
Integral Derivative ( PID ) form.

**PolynomialRateFilter** instances approximate a signal evaluated at an effective
frequency equal to the product of the normalized frequency and a rate greater
than or equal to one, supporting interpolation through localized polynomial
approximation with no group delay.
		
**PolyphaseRateFilter** instances approximate a signal evaluated at an effective
frequency equal to the product of the normalized frequency and a rate greater
than zero, supporting decimation and interpolation through construction and
application of a polyphase filter bank, a sequence of low pass filters with a
common frequency response and a fractional sample difference in group delay.  An
appropriate stride is determined to realize the specified effective frequency
without bias and with group delay based on order.

**RankFilter** instances define nonlinear morphological operators, which define
functionality based on rank and order, including dilation, median, and erosion,
and may be combined in sequences to support close and open.
		
**WindowFilter** instances realize discrete window functions useful in Fourier
analysis, based on type, classification, order, and normalization, through
extensible factory construction.
		
#### [interfaces](https://larryturner.github.io/diamondback/diamondback.interfaces)

**IA**, **IB**, **IClear**, **IData**, **IDateTime**, **IDuration**,
**IEncoding**, **IEqual**, **IFrequency**, **IInterval**, **ILatency**,
**IPath**, **IPeriod**, **IPhase**, **IQ**, **IRate**, **IReset**,
**IResolution**, **IRotation**, **IS**, **IState**, **ITimeZone**, and
**IUpdate** interfaces facilitate mix-in design.
	
#### [models](https://larryturner.github.io/diamondback/diamondback.models)

**DiversityModel** instances select and retain a state extracted to maximize the
minimum distance between state members based on classification and order,
through extensible factory construction.  An opportunistic unsupervised learning
model typically improves condition and numerical accuracy and reduces storage
relative to alternative approaches including generalized linear inverse.

**PrincipalComponentModel** instances are supervised learning models which
analyze an incident signal to learn a mean vector, standard deviation vector,
and a collection of eigenvectors, and produce a reference signal which is a
candidate for dimension reduction, in which higher order dimensions are
discarded, reducing the order of the reference signal, while preserving
significant and often sufficient information.
		
#### [transforms](https://larryturner.github.io/diamondback/diamondback.transforms)
	
**ComplexTransform** is a singleton instance which converts a three-phase real
signal to a complex signal, or a complex signal to a three-phase real signal, in
equivalent and reversible representations, based on a neutral condition.
		
**FourierTransform** is a singleton instance which converts a real or complex
discrete-time signal to a complex discrete-frequency signal, or a complex
discrete-frequency signal to a real or complex discrete-time signal, in
equivalent and reversible representations, based on a window filter and inverse.
		
**PowerSpectrumTransform** is a singleton instance which converts a real or complex
discrete-time signal to a real discrete-frequency signal which estimates a mean
power density of the signal, based on a window filter.
		
**WaveletTransform** instances realize a temporal spatial frequency transformation
through construction and application of analysis and synthesis filters with
complementary frequency responses, combined with downsampling and upsampling
operations, in equivalent and reversible representations.  A factory constructs
instances based on type, classification, and order.  Filters may be readily
extended to support new types and functionality, while retaining factory
support.

**ZTransform** is a singleton instance which converts continuous s-domain to
discrete z-domain difference equations, based on a normalized frequency and
application of bilinear or impulse invariant methods.	
	
### Dependencies

Diamondback depends upon external packages :
    
* [jsonpickle](https://github.com/jsonpickle/jsonpickle)
    
* [numpy](https://github.com/numpy/numpy)
    
* [scipy](https://github.com/scipy/scipy)

Diamondback Jupyter notebook depends upon additional external packages :

* [ipython](https://github.com/ipython/ipython)

* [ipywidgets](https://github.com/jupyter-widgets/ipywidgets)

* [jupyter](https://github.com/jupyter/notebook)

* [matplotlib](https://github.com/matplotlib/matplotlib)

* [pillow](https://github.com/python-pillow/pillow)

### Installation

Diamondback is a public repository hosted at PyPI and GitHub.

    pip install diamondback

    pip install git+https://github.com/larryturner/diamondback.git
	
### Demonstration

A Jupyter notebook defines cells to create and exercise diamondback components.
The notebook serves as a simplified but useful introduction to and
demonstration of diamondback capabilities.

A Jupyter notebook may be run on a remote server without installation on
Binder, which dynamically builds and deploys a Docker container from a GitHub
repository, or installed from GitHub and run on a local system.

* Remote. 

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/larryturner/diamondback/master?filepath=jupyter%2Fdiamondback.ipynb)

* Local.

    git clone https://github.com/larryturner/diamondback.git

    cd diamondback
    
    pip install --requirement requirements.txt
    
    jupyter notebook .\jupyter\diamondback.ipynb

Restart the kernel, as the first cell contains common definitions, find cells
which exercise components of interest, and manipulate widgets to exercise and
visualize functionality.
    
### Documentation

Diamondback documentation is generated from the source, indexed, and searchable.
  
[GitHub](https://larryturner.github.io/diamondback/)
        
### Test

A simple pytest solution is provided to exercise and verify diamondback
components.
	
    py.test -v --capture=no .\test
	
### Author

[Larry Turner](https://github.com/larryturner)
	
### License

[BSD-3C](https://github.com/larryturner/diamondback/blob/master/license)

### Release

[Version](https://github.com/larryturner/diamondback/blob/master/version)
        
Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.
	