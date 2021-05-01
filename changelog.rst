=======
Release
=======

1.0.6 - 2019-09-08
^^^^^^^^^^^^^^^^^^

-   Initial release.

1.0.7 - 2019-10-23
^^^^^^^^^^^^^^^^^^

-   Modified exception formatting.

1.0.8 - 2020-01-09
^^^^^^^^^^^^^^^^^^

-   Modified Serial encode exceptions.

1.0.9 - 2020-01-13
^^^^^^^^^^^^^^^^^^

-   Modified jupyter notebook Pillow import.

1.0.10 - 2020-03-08
^^^^^^^^^^^^^^^^^^^

-   Modified comments.

1.0.11 - 2020-05-13
^^^^^^^^^^^^^^^^^^^

-   Modified Log to define and display time zone.

-   Added IData, IDateTime, IDuration, IEncoding, IInterval, ILatency, IPath,
    IPeriod, IResolution, IRotation, IState, and ITimeZone.

1.0.12 - 2020-05-14
^^^^^^^^^^^^^^^^^^^

-   Added IUpdate.

1.0.13 - 2020-05-19
^^^^^^^^^^^^^^^^^^^

-   Modified IDateTime.

1.0.14 - 2020-07-15
^^^^^^^^^^^^^^^^^^^

-   Modified Log to integrate reentrant thread safety.

1.0.15 - 2020-07-22
^^^^^^^^^^^^^^^^^^^

-   Modified jupyter notebook to utilize Open CV, and eliminate pillow
    dependency.

1.0.16 - 2020-07-27
^^^^^^^^^^^^^^^^^^^

-   Modified documentation.

1.0.17 - 2020-08-06
^^^^^^^^^^^^^^^^^^^

-   Modified Log to improve exception formatting.

-   Modified jupyter notebook to utilize warnings to ignore import deprecation
    warnings.

1.0.18 - 2020-08-11
^^^^^^^^^^^^^^^^^^^

-   Modified jupyter notebook to improve appearance.

1.0.19 - 2020-08-18
^^^^^^^^^^^^^^^^^^^

-   Modified jupyter notebook to utilize pillow, and eliminate open dependency.

-   Modified documentation to run jupyter notebook with binder.

1.0.20 - 2020-08-19
^^^^^^^^^^^^^^^^^^^

-   Modified documentation.

-   Modified jupyter notebook to embed images and improve links.

1.0.21 - 2020-08-19
^^^^^^^^^^^^^^^^^^^

-   Modified PolynomialRateFilter to support decimation and interpolation.

1.0.22 - 2020-08-26
^^^^^^^^^^^^^^^^^^^

-   Modified documentation.

1.0.23 - 2020-09-09
^^^^^^^^^^^^^^^^^^^

-   Modified documentation, replaced sphinx theme.

1.0.24 - 2020-09-23
^^^^^^^^^^^^^^^^^^^

-   Added IVersion.

-   Modified requirements.

1.0.25 - 2020-10-12
^^^^^^^^^^^^^^^^^^^

-   Added nox sessions with dist, docs, push, and tests methods.

1.0.26 - 2020-10-13
^^^^^^^^^^^^^^^^^^^

-   Added ICache, IProxy, and IUrl.

1.0.27 - 2020-10-21
^^^^^^^^^^^^^^^^^^^

-   Added type hints and modified documentation.

-   Renamed IDateTime to IDate to avoid datetime conflict.

-   Added ICompress, IConnect, IDispose, IEmulate, IStream, IValid, and IWrite.

-   Added clients subpackage and RestClient.

1.0.28 - 2020-10-27
^^^^^^^^^^^^^^^^^^^

-   Added IConfigure.

-   Modified RequestClient in extend requests support, reduce external
    dependencies, and add data.

-   Modified Serial to add support for pandas and register extensions.

1.0.29 - 2020-11-02
^^^^^^^^^^^^^^^^^^^

-   Modified RestClient to remove user and added IUser.

1.0.30 - 2020-11-04
^^^^^^^^^^^^^^^^^^^

-   Modified nox, dependencies, and documentation.

1.0.31 - 2020-11-06
^^^^^^^^^^^^^^^^^^^

-   Modified Serial encode and decode disable compression as default.

-   Modified RestClient to strip leading and trailing '/' from URL and API
    properties and arguments.

1.0.32 - 2020-11-09
^^^^^^^^^^^^^^^^^^^

-   Modified RestClient to force coercion of item dictionary values to strings.

1.0.33 - 2020-11-10
^^^^^^^^^^^^^^^^^^^

-   Added IIdentity.

1.0.34 - 2020-11-11
^^^^^^^^^^^^^^^^^^^

-   Modified RestClient to add json and binary data body support.

1.0.35 - 2020-11-16
^^^^^^^^^^^^^^^^^^^

-   Modified RestClient request to add timeout.

1.0.36 - 2020-11-19
^^^^^^^^^^^^^^^^^^^

-   Modified RestClient cache and live, and deprecate ready.

1.0.37 - 2020-11-19
^^^^^^^^^^^^^^^^^^^

-   Modified RestClient cache.

1.0.38 - 2020-11-20
^^^^^^^^^^^^^^^^^^^

-   Modified RestClient live.

-   Modified init to simplify import, eliminating required package declaration.

1.0.39 - 2020-11-25
^^^^^^^^^^^^^^^^^^^

-   Modified IClear, IReset, and IUpdate.

-   Renamed IState to IModel.

1.0.40 - 2020-12-11
^^^^^^^^^^^^^^^^^^^

-   Modified IUser to recover from getpass failure.

1.0.41 - 2020-12-11
^^^^^^^^^^^^^^^^^^^

-   Modified requirements.

1.0.42 - 2021-01-06
^^^^^^^^^^^^^^^^^^^

-   Modified RestClient request timeout.

1.0.43 - 2021-01-07
^^^^^^^^^^^^^^^^^^^

-   Modified RestClient request retry status 5xx.

1.0.44 - 2021-01-07
^^^^^^^^^^^^^^^^^^^

-   Modified RestClient request retry status 5xx.

1.0.45 - 2021-01-07
^^^^^^^^^^^^^^^^^^^

-   Modified RestClient request Log entries.

1.0.46 - 2021-01-08
^^^^^^^^^^^^^^^^^^^

-   Added ICount.

1.0.47 - 2021-01-08
^^^^^^^^^^^^^^^^^^^

-   Modified RestClient request to delay on retry.

1.0.48 - 2021-01-12
^^^^^^^^^^^^^^^^^^^

-   Added ILive and IReady.

-   Modified RestClient to use ILive, IReady, IUser, and IVersion.

-   Modified RestClient request to deprecate retry and migrate cache
    specification.

1.0.49 - 2021-01-15
^^^^^^^^^^^^^^^^^^^

-   Modified RestClient to return binary data on JSON conversion exception.

1.0.50 - 2021-01-17
^^^^^^^^^^^^^^^^^^^

-   Modified Log and RestClient Lock.

1.0.51 - 2021-01-18
^^^^^^^^^^^^^^^^^^^

-   Modified Log and RestClient RLock.

1.0.52 - 2021-01-20
^^^^^^^^^^^^^^^^^^^

-   Added ITimeOut.

-   Modified RestClient to use ITimeOut.

1.0.53 - 2021-01-21
^^^^^^^^^^^^^^^^^^^

-   Modified RestClient request to return JSON, binary, or text response.

1.0.54 - 2021-01-26
^^^^^^^^^^^^^^^^^^^

-   Modified RestClient to use IClear.

1.0.55 - 2021-02-01
^^^^^^^^^^^^^^^^^^^

-   Added IAsset.

1.0.56 - 2021-02-01
^^^^^^^^^^^^^^^^^^^

-   Modified requirements.

1.0.57 - 2021-02-01
^^^^^^^^^^^^^^^^^^^

-   Modified requirements, removed pytz dependency.

1.0.58 - 2021-02-03
^^^^^^^^^^^^^^^^^^^

-   Modified RestClient to remove IUser.

1.0.59 - 2021-02-03
^^^^^^^^^^^^^^^^^^^

-   Modified documentation.

1.0.60 - 2021-02-08
^^^^^^^^^^^^^^^^^^^

-   Modified RestClient live, ready, and version.

-   Modified IUrl.

1.0.61 - 2021-02-16
^^^^^^^^^^^^^^^^^^^

-   Modified RestClient.

1.0.62 - 2021-02-26
^^^^^^^^^^^^^^^^^^^

-   Modified Serial code.

1.0.63 - 2021-03-02
^^^^^^^^^^^^^^^^^^^

-   Modified Log to use loguru and deprecate logging.

1.0.64 - 2021-03-02
^^^^^^^^^^^^^^^^^^^

-   Modified Log to define any entry.

1.0.65 - 2021-03-03
^^^^^^^^^^^^^^^^^^^

-   Modified Log format.

1.0.66 - 2021-03-03
^^^^^^^^^^^^^^^^^^^

-   Modified Log exceptions.

1.0.67 - 2021-03-03
^^^^^^^^^^^^^^^^^^^

-   Modified RestClient package.

1.0.68 - 2021-03-03
^^^^^^^^^^^^^^^^^^^

-   Modified jupyter.

1.0.69 - 2021-03-05
^^^^^^^^^^^^^^^^^^^

-   Modified strings to F-strings.

1.0.70 - 2021-03-05
^^^^^^^^^^^^^^^^^^^

-   Modified jupyter.

1.0.71 - 2021-03-12
^^^^^^^^^^^^^^^^^^^

-   Modified RestClient exceptions.

1.0.72 - 2021-03-14
^^^^^^^^^^^^^^^^^^^

-   Modified RestClient to use IHeader, deprecate caching and return requests
    response.

1.0.73 - 2021-03-15
^^^^^^^^^^^^^^^^^^^

-   Added ILabel.

1.0.74 - 2021-03-15
^^^^^^^^^^^^^^^^^^^

-   Modified init.

1.0.75 - 2021-03-16
^^^^^^^^^^^^^^^^^^^

-   Modified Serial to use base-85 encoded gzip JSON, and compact separators.

1.0.76 - 2021-03-25
^^^^^^^^^^^^^^^^^^^

-   Modified FirFilter and IirFilter to deprecate use of IRate.

1.0.77 - 2021-03-25
^^^^^^^^^^^^^^^^^^^

-   Modified IirFilter filter.

1.0.78 - 2021-03-30
^^^^^^^^^^^^^^^^^^^

-   Modified documentation.

1.0.79 - 2021-04-01
^^^^^^^^^^^^^^^^^^^

-   Modified interface initializations.

1.0.80 - 2021-04-13
^^^^^^^^^^^^^^^^^^^

-   Modified Log format and added lazy initialization of loguru.

1.0.81 - 2021-04-13
^^^^^^^^^^^^^^^^^^^

-   Modified Log minimum level.

1.0.82 - 2021-04-14
^^^^^^^^^^^^^^^^^^^

-   Modified documentation.

1.0.83 - 2021-04-23
^^^^^^^^^^^^^^^^^^^

-   Modified requirements.

1.0.84 - 2021-04-28
^^^^^^^^^^^^^^^^^^^

-   Modified requirements to remove dateutil.

1.0.85 - 2021-05-02
^^^^^^^^^^^^^^^^^^^

-   Modified typing and cleaned declarations.

-   Removed IUser.
