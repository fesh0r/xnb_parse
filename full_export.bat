@echo off

if exist Content\Essentials.pak if exist Content\Other.pak goto content
echo *** Essentials.pak and Other.pak not found in Content
goto music

:content
echo Checking for XNA runtime
call xna_native.bat 2>NUL
if errorlevel 1 goto no_xna

echo Decompressing Essentials.pak and Other.pak...
call fez_decomp.bat Content out
if errorlevel 1 goto error
goto convert

:no_xna
echo Unpacking Essentials.pak and Other.pak...
call fez_unpack.bat Content out_c
if errorlevel 1 goto error

echo Decompressing XNBs...
call xnb_decomp_net.bat out_c out
if errorlevel 1 goto error

:convert
echo Converting XNBs...
call read_xnb_dir.bat out export
if errorlevel 1 goto error

:music
if exist Content\Music.pak goto music_pak
if exist "Content\Music\XACT Music.xgs" if exist "Content\Music\Sound Bank.xsb" if exist "Content\Music\Sound Bank.xsb" goto music_xact
echo *** Music.pak or Music folder not found in Content
goto end

:music_pak
echo Extracting Music.pak...
call fez_music_unpack.bat Content export\Music
if errorlevel 1 goto error

echo Decoding OGGs...
call ogg_decode.bat export

goto end

:music_xact
echo Converting XACT Music...
call read_xact.bat "Content\Music\XACT Music.xgs" "Content\Music\Sound Bank.xsb" "Content\Music\Wave Bank.xwb" export\Music
if errorlevel 1 goto error

echo Decoding XMAs...
call xma_decode.bat export

echo Decoding xWMAs...
call xwma_decode.bat export

goto end

:error
echo *** BANG ***
exit /b 1

:end
