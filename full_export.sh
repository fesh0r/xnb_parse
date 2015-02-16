#!/bin/sh

if ! command -v python 2>&1 >/dev/null
then
	echo "*** python required"
	exit 1
fi

if ! python xna_native.py 2>/dev/null
then
	if ! command -v mono 2>&1 >/dev/null
	then
		echo "*** mono required"
		exit 1
	fi
fi

if [ -e "Content/Essentials.pak" -a -e "Content/Other.pak" ]
then
	if python xna_native.py 2>/dev/null
	then
		echo "Decompressing Essentials.pak and Other.pak..."
		python fez_decomp.py Content out || exit 1
	else
		echo "Unpacking Essentials.pak and Other.pak..."
		python fez_unpack.py Content out_c || exit 1

		echo "Decompressing XNBs..."
		mono bin/xnbdecomp.exe out_c out || exit 1
	fi

	echo "Converting XNBs..."
	python read_xnb_dir.py out export || exit 1
else
	echo "*** Essentials.pak and Other.pak not found in Content"
fi

if [ -e "Content/Music.pak" ]
then
	echo "Extracting Music.pak..."
	python fez_music_unpack.py Content export/music || exit 1
elif [ -e "Content/Music/XACT Music.xgs" -a -e "Content/Music/Sound Bank.xsb" -a -e "Content/Music/Wave Bank.xwb" ]
then
	echo "Converting XACT Music..."
	python read_xact.py "Content/Music/XACT Music.xgs" "Content/Music/Sound Bank.xsb" "Content/Music/Wave Bank.xwb" export/music || exit 1
else
	echo "*** Music.pak or Music folder not found in Content"
fi
