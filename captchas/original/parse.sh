#!/bin/bash

mkdir -p ../cropped/soup
mkdir -p ../letters

for i in *.gif; do
	NAME=`basename $i .gif`
	echo '[i] Crop the image'
	convert -fill white +opaque black -crop 165x60+20 "$i" "../cropped/$NAME.gif"

	convert -crop "6x1@" "../cropped/$NAME.gif" "../cropped/$NAME.png"
	mogrify -trim "../cropped/$NAME-*.png"
	for j in $(seq 0 5); do
		CHARACTER=${NAME:j:1}
		mkdir -p "../letters/$CHARACTER"
		mv "../cropped/${NAME}-${j}.png" "../letters/$CHARACTER/$NAME.png"
		# mv "../cropped/$NAME-cropped-$j.gif" "../letters/$CHARACTER/$NAME.gif"
	done
done
