#!/bin/bash

echo "Unpacking Essentials.pak and Other.pak..."
python fez_unpack.py Content out_c

echo "Decompressing XNBs..."
mono bin/xnbdecomp.exe out_c out

echo "Converting XNBs..."
python read_xnb_dir.py out export

if [ -e "Content/Music.pak" ]
then
	echo "Extracting Music.pak..."
	python fez_music_unpack.py Content export/music
else
	echo "Converting XACT Music..."
	python read_xact.py "Content/Music/XACT Music.xgs" "Content/Music/Sound Bank.xsb" "Content/Music/Wave Bank.xwb" export/music
fi
