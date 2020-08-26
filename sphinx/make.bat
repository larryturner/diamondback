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

:: Parameters

set destinationpath=..\docs

set build=sphinx-build

set sourcepath=source

set options=-d %buildpath%\doctrees

:: Clean

if "%1" == "clean" (

    for /d %%i in (%destinationpath%\*) do rmdir /q /s %%i

    del /q /s %destinationpath%\*
    
    goto end
)

:: Help

if "%1" == "help" (

    echo make ^<target^>

    echo       clean    - delete documentation.

    echo       html     - create documentation.

    goto end
)

:: HTML

if "%1" == "html" (
    
    %build% -b html %options% %sourcepath% %destinationpath%
        
    goto end
)

:end
