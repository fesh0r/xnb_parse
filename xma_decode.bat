@echo off
setlocal
set BIN_DIR=%~dp0bin\

if exist %BIN_DIR%xma2encode.exe goto xma2
if exist %BIN_DIR%xmaencode.exe goto xma
echo *** xmaencode.exe or xma2encode.exe required to decode xma files ***
exit /B 1

:xma2
for /R %1 %%F in (*.xma) do %BIN_DIR%xma2encode.exe "%%F" /DecodeToPCM "%%~dpnF.wav" /Verbose
goto end

:xma
for /R %1 %%F in (*.xma) do %BIN_DIR%xmaencode.exe "%%F" /X "%%~dpnF.wav" /V
goto end

:end
