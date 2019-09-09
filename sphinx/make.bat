::  Description
::
::      Sphinx documentation management.
::
::  License
::
::      BSD-3C.
::
::      Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.
::
::  Author
::
::      Larry Turner, Schneider Electric, Analytics & AI, 2018-01-23.
::
::  Definition

@echo off

set BUILDDIR=..\docs

set SOURCEDIR=source

set SPHINXBUILD=sphinx-build

set ALLSPHINXOPTS=-d %BUILDDIR%\doctrees %SPHINXOPTS%

if "%1" == "clean" (

    for /d %%i in (%BUILDDIR%\*) do rmdir /q /s %%i

    del /q /s %BUILDDIR%\*
    
    goto end
)

if "%1" == "html" (
    
    %SPHINXBUILD% -b html %ALLSPHINXOPTS% %SOURCEDIR% %BUILDDIR%
        
    goto end
)

echo make ^<target^>
    
echo       clean    remove HTML files
    
echo       html     create HTML files

:end