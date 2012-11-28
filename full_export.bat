@echo off

echo Decompressing Essentials.pak and Other.pak...
call fez_decomp.bat Content out
if %errorlevel% neq 0 goto error

echo Converting XNBs...
call read_xnb_dir.bat out export
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
