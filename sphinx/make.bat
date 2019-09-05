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