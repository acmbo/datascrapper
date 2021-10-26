#!/bin/bash

for file in ./*.py ; do 
	echo "Diese Datei: $file"
	fname=$(basename "$file")
	echo "hat den Namen: $fname"
	fdir=$(dirname "$file")
	echo "und steht im Verzeichnis: $fdir"
done