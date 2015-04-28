#!/bin/bash
rm -rf cropped captchas
mkdir -p captchas glyphs cropped
CAPTCHA_URL="http://www.indiapost.gov.in/captcha.aspx"

for (( i = 1; i < 4; i++ )); do
  wget -q $CAPTCHA_URL -O "captchas/$i.gif"
  python extract.py "captchas/$i.gif"
done

rm -rf captchas
fdupes --delete -N cropped/

cd glyphs
mkdir -p 0 1 2 3 4 5 6 7 8
cd ..
