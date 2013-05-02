@echo off
setlocal
set BIN_DIR=%~dp0bin\

if exist %BIN_DIR%oggdec.exe goto ogg
echo *** oggdec.exe required to decode ogg files ***
exit /B 1

:ogg
for /R %1 %%F in (*.ogg) do %BIN_DIR%oggdec.exe "%%F" -w "%%~dpnF.wav"
goto end

:end
