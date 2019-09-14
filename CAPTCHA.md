# Captcha Details

There are 3 kind of captchas that the India Post website shows:

## Math Evaluations

![](captchas/test/a.png)

![](captchas/test/c.png)

## Pick a Character

![](captchas/test/b.png)

## Standard Captcha

![](captchas/test/test.gif)

This package breaks all 3 of these. The first 2 are solved using Tesseract (force a limited charset, and force it to be detected as a single line). The third one is solved using a [Vector Space Search Engine implementation][1].

The code is available in captcha.py and textcaptcha.py. The cleanup of text captcha images is done using simple imagemagick commands.

[1]: https://boyter.org/decoding-captchas/
