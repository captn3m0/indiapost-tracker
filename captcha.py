import glob
import os

from PIL import Image

from compare import VectorCompare

###########################
# Load the training set
# 
###########################
DICTIONARY = {}
for x in range(0, 9):
    DICTIONARY[str(x)] = []


def buildvector(im):
    d1 = {}
    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1
    return d1


for filename in glob.iglob('glyphs/**/*'):
    c = os.path.basename(os.path.dirname(filename))
    DICTIONARY[c].append(buildvector(Image.open(filename)))


##############################
# Now we keep making requests to the captcha

# Now we break the captcha

class Captcha(object):
    def __init__(self, filename):
        super(Captcha, self).__init__()
        self.letters = []
        self.im = Image.open(filename)
        # self.im = self.im.convert("P")
        self.im2 = Image.new("P", self.im.size, 255)
        # self.im = self.im.convert("P")
        self.clean_image()
        self.extract_letters()

    def clean_image(self):
        temp = {}

        for x in range(self.im.size[1]):
            for y in range(self.im.size[0]):
                pix = self.im.getpixel((y, x))
                temp[pix] = pix
                if pix < 60:  # these are the numbers to get
                    self.im2.putpixel((y, x), 0)

    def extract_letters(self):
        inletter = False
        foundletter = False
        start = 0
        end = 0

        # im2 now has black captcha

        for y in range(self.im2.size[0]):  # slice across
            for x in range(self.im2.size[1]):  # slice down
                pix = self.im2.getpixel((y, x))
                if pix != 255:
                    inletter = True
            if foundletter == False and inletter == True:
                foundletter = True
                start = y

            if foundletter == True and inletter == False:
                foundletter = False
                end = y
                self.letters.append((start, end))

            inletter = False

    def crack(self):
        # letters now contains the cordinates
        v = VectorCompare()
        captcha = ""

        for index, letter in enumerate(self.letters):
            im3 = self.im2.crop((letter[0], 0, letter[1], self.im2.size[1]))
            buestguess = 0
            solution = None

            for character in DICTIONARY:
                list = DICTIONARY[character]

                for vector in list:
                    score = v.relation(vector, buildvector(im3))

                    if score > buestguess:
                        solution = character
                        buestguess = score
            captcha += solution

        return captcha
