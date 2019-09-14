from PIL import Image
from vectorcompare import VectorCompare
import subprocess
import tempfile
import os
import sys

v = VectorCompare()

def buildvector(im):
    d1 = {}
    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1
    return d1

class CaptchaOracle:

    # Directory is the directory with all the captchas
    def __init__(self, directory=""):
        self.imageset = []

        iconset = ['1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']

        for letter in iconset:
            letterset = []
            for img in os.listdir("%s/%s"%(directory, letter)):
                v = buildvector(Image.open("%s/%s/%s"%(directory, letter, img)))
                self.imageset.append({"letter":letter,"v": v, "img": img})

    def guesses(self, vector):
        guesses = []
        for data in self.imageset:
            guesses.append(
                (
                    v.relation(data["v"], vector),
                    data["letter"],
                    data["img"]
                )
            )
        guesses.sort(reverse=True)
        return guesses

oracle = CaptchaOracle("./captchas/letters")

class Captcha:
    def __init__(self, filename):
        fp = tempfile.NamedTemporaryFile(suffix=".gif")
        self.d = tempfile.mkdtemp()
        subprocess.run(["convert", "-fill", "white", "+opaque", "black", "-crop", "165x60+20", filename, fp.name])
        subprocess.run(["convert", "-crop", "6x1@", fp.name, self.d + "/captcha.png"])
        subprocess.run(["mogrify", "-trim", self.d + "/captcha-*.png"])

    def break_images(self):
        vectors = []
        for x in range(0,6):
            file = "%s/captcha-%s.png"%(self.d, x)
            im = Image.open(file)
            vectors.append(buildvector(im))
        return vectors

    def solve(self):
        word = ""
        vectors = self.break_images()
        for vector in vectors:
            guesses = oracle.guesses(vector)
            word += guesses[0][1]
        return word

