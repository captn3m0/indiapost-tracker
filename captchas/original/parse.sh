#!/bin/bash

for i in *.gif; do
	NAME=`basename $i .gif`
	echo '[i] Crop the image'
	convert -fill white +opaque black -crop 165x60+20 "$i" "../cropped/$NAME.gif"
done
