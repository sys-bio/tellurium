@echo off
set WINPYDIRBASE=%~dp0..
rem get a normalize path
CALL :NORMALIZEPATH "%WINPYDIRBASE%"
set WINPYDIRBASE=%RETVAL%
set RETVAL=

set WINPYDIR=%WINPYDIRBASE%\python-2.7.13.amd64

set WINPYVER=2.7.13.0Zero
set HOME=%WINPYDIRBASE%\settings
set WINPYDIRBASE=

set JUPYTER_DATA_DIR=%HOME%
set WINPYARCH=WIN32
if  "%WINPYDIR:~-5%"=="amd64" set WINPYARCH=WIN-AMD64
set FINDDIR=%WINDIR%\system32
echo ;%PATH%; | %FINDDIR%\find.exe /C /I ";%WINPYDIR%\;" >nul
if %ERRORLEVEL% NEQ 0 set PATH=%WINPYDIR%\Lib\site-packages\PyQt5;%WINPYDIR%\Lib\site-packages\PyQt4;%WINPYDIR%\;%WINPYDIR%\DLLs;%WINPYDIR%\Scripts;%WINPYDIR%\..\tools;%WINPYDIR%\..\tools\mingw32\bin;%WINPYDIR%\..\tools\R\bin\x64;%WINPYDIR%\..\tools\Julia\bin;%WINPYDIR%\..\tools\Graphviz2.38\bin;%PATH%;

rem force default pyqt5 kit for Spyder if PyQt5 module is there
if exist "%WINPYDIR%\Lib\site-packages\PyQt5\__init__.py" set QT_API=pyqt5

rem ******************
rem handle R if included
rem ******************
if not exist "%WINPYDIR%\..\tools\R\bin" goto r_bad
set R_HOME=%WINPYDIR%\..\tools\R
if     "%WINPYARCH%"=="WIN32" set R_HOMEbin=%R_HOME%\bin\i386
if not "%WINPYARCH%"=="WIN32" set R_HOMEbin=%R_HOME%\bin\x64
:r_bad


rem ******************
rem handle Julia if included
rem ******************
if not exist "%WINPYDIR%\..\tools\Julia\bin" goto julia_bad
set JULIA_HOME=%WINPYDIR%\..\tools\Julia\bin\
set JULIA_EXE=julia.exe
set JULIA=%JULIA_HOME%%JULIA_EXE%
set JULIA_PKGDIR=%WINPYDIR%\..\settings\.julia
:julia_bad

rem ******************
rem WinPython.ini part (removed from nsis)
rem ******************
if not exist "%WINPYDIR%\..\settings" mkdir "%WINPYDIR%\..\settings" 
set winpython_ini=%WINPYDIR%\..\settings\winpython.ini
if not exist "%winpython_ini%" (
    echo [debug]>>"%winpython_ini%"
    echo state = disabled>>"%winpython_ini%"
    echo [environment]>>"%winpython_ini%"
    echo ## <?> Uncomment lines to override environment variables>>"%winpython_ini%"
    echo #HOME = %%HOMEDRIVE%%%%HOMEPATH%%\Documents\WinPython%%WINPYVER%%>>"%winpython_ini%"
    echo #JUPYTER_DATA_DIR = %%HOME%%>>"%winpython_ini%"
    echo #WINPYWORKDIR = %%HOMEDRIVE%%%%HOMEPATH%%\Documents\WinPython%%WINPYVER%%\Notebooks>>"%winpython_ini%"
)

rem *****
rem http://stackoverflow.com/questions/1645843/resolve-absolute-path-from-relative-path-and-or-file-name
rem *****
:: ========== FUNCTIONS ==========
EXIT /B

:NORMALIZEPATH
  SET RETVAL=%~dpfn1
  EXIT /B

