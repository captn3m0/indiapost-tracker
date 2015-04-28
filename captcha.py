from PIL import Image
import glob
import os
import sys
from compare import VectorCompare
###########################
# Load the training set
# 
###########################
DICTIONARY = {}
for x in xrange(0, 9):
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
im = Image.open(sys.argv[1])
im = im.convert("P")
im2 = Image.new("P",im.size,255)
im = im.convert("P")

temp = {}

for x in range(im.size[1]):
  for y in range(im.size[0]):
    pix = im.getpixel((y,x))
    temp[pix] = pix
    if pix <60: # these are the numbers to get
      im2.putpixel((y,x),0)

inletter = False
foundletter=False
start = 0
end = 0

# im2 now has black captcha
letters = []

for y in range(im2.size[0]): # slice across
  for x in range(im2.size[1]): # slice down
    pix = im2.getpixel((y,x))
    if pix != 255:
      inletter = True
  if foundletter == False and inletter == True:
    foundletter = True
    start = y

  if foundletter == True and inletter == False:
    foundletter = False
    end = y
    letters.append((start,end))

  inletter=False

# letters now contains the cordinates
# 
v = VectorCompare()
captcha = ""

for index, letter in enumerate(letters):  
  im3 = im2.crop(( letter[0] , 0, letter[1],im2.size[1] ))
  buestguess = 0
  solution = None

  for character in DICTIONARY:
    list = DICTIONARY[character]

    for vector in list:
      score = v.relation(vector, buildvector(im3))

      if score > buestguess:
        solution = character
        buestguess = score
  captcha+=solution

print captcha