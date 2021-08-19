# python-numpy-messing-about
just some messing about with python and numpy and template matching
for now a couple of weird ones:

blurry-text-ocr.py - ocr through template matching -- my attempt at figuring out what the somewhat blurry (but not too blurry) text is based on extracted letter from the same text which I can correctly identify w/ 100% certainty , code adjusted ever so slightly from here: https://stackoverflow.com/questions/50579050/template-matching-with-multiple-objects-in-opencv-python

cards-part1-done.py - basically matching detected parts of a whole image, but then using textual identification/output -- the idea was to get the layout of a poker table and match all the shown cards, and then to put the value of those cards through poker odds calculator api, it's kinda finished btw. the code is like a bad horror movie :) , also I just can't find the patience to get images of all 52 cards and properly format/crop them, but once I do that, I'll put it here for reference
