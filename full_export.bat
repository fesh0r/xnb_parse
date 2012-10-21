call fez_unpack.bat Content\Essentials.pak out
if %errorlevel% neq 0 goto error

call fez_unpack.bat Content\Other.pak out
if %errorlevel% neq 0 goto error

call xnb_decomp.bat out out_u
if %errorlevel% neq 0 goto error

call read_xnb_dir.bat out_u export
if %errorlevel% neq 0 goto error

call xma_decode.bat export
if %errorlevel% neq 0 goto error

pause

goto end

:error
echo BANG
exit /b 1

:end
