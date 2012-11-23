@echo off

echo Unpacking Essentials.pak...
call fez_unpack.bat Content\Essentials.pak out
if %errorlevel% neq 0 goto error

echo Unpacking Other.pak...
call fez_unpack.bat Content\Other.pak out
if %errorlevel% neq 0 goto error

echo Decompressing XNBs...
call xnb_decomp.bat out out_u
if %errorlevel% neq 0 goto net_decomp
goto conv
:net_decomp
echo Trying .net decompressor
bin\xnbdecomp.exe out out_u
if %errorlevel% neq 0 goto error
goto error

:conv
echo Converting XNBs...
call read_xnb_dir.bat out_u export
if %errorlevel% neq 0 goto error

echo Converting XWB...
call read_xact.bat "Content\Music\Wave Bank.xwb" export\Music

echo Decoding XMAs...
call xma_decode.bat export

echo Decoding xWMAs...
call xwma_decode.bat export

pause

goto end

:error
echo *** BANG ***
exit /b 1

:end
