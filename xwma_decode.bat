@echo off
setlocal
set BIN_DIR=%~dp0bin\

if exist %BIN_DIR%xwmaencode.exe goto xwma
echo *** xwmaencode.exe required to decode xwma files ***
exit /B 1

:xwma
for /R %1 %%F in (*.xwma) do %BIN_DIR%xwmaencode.exe "%%F" "%%~dpnF.wav"
goto end

:end
