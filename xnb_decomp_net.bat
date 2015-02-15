@echo off
setlocal
set BIN_DIR=%~dp0bin\

if exist %BIN_DIR%xnbdecomp.exe goto xnbdecomp
echo *** xnbdecomp.exe required to decompress XNB files ***
exit /B 1

:xnbdecomp
%BIN_DIR%xnbdecomp.exe %1 %2
goto end

:end
