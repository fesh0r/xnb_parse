@echo off

echo Decompressing Essentials.pak and Other.pak...
call fez_decomp.bat Content out
if %errorlevel% neq 0 goto error

echo Converting XNBs...
call read_xnb_dir.bat out export
rem if %errorlevel% neq 0 goto error

if exist Content\Music.pak (
    echo Extracting Music.pak...
    call fez_music_unpack.bat Content export\Music

    echo Decoding OGGs...
    call ogg_decode.bat export
) else (
    echo Converting XACT Music...
    call read_xact.bat "Content\Music\XACT Music.xgs" "Content\Music\Sound Bank.xsb" "Content\Music\Wave Bank.xwb" export\Music

    echo Decoding XMAs...
    call xma_decode.bat export

    echo Decoding xWMAs...
    call xwma_decode.bat export
)

pause

goto end

:error
echo *** BANG ***
exit /b 1

:end
