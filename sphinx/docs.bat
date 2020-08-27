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

set build=sphinx-build

set documentpath=..\docs

set imagepath=..\images

set sourcepath=source

set options=-d %documentpath%\doctrees

:: Clean

if "%1" == "clean" (

    for /d %%i in (%documentpath%\*) do rmdir /q /s %%i

    del /q /s %documentpath%\*
    
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
    
    %build% -b html %options% %sourcepath% %documentpath%

    xcopy /E /I /Y %imagepath% %documentpath%\images

    goto end
)

:end
