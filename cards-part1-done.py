import cv2
import numpy as np
import glob
import re
import sys
import warnings

warnings.filterwarnings('ignore')  # has to be done otherwise due to later part of the code it will pop a warning
#from textops import *

#empty list to store template images
template_data=[]
template_names = []
#make a list of all template images from a directory, my images were named as per cards cmp-[Ac].png for Ace of Clubs, etc.
files1= glob.glob('cmp-[*.png')  

class MyImage:
    def __init__(self, img_name):
        self.img = cv2.imread(img_name)
        self.__name = img_name

    def __str__(self):
        return self.__name
        
for myfile in files1:
    image = cv2.imread(myfile,0)
    image_name = MyImage(myfile)
    template_data.append(image)
    template_names.append(image_name)
    #print(image, image_name)

test_image = cv2.imread('og2-test.png') # a poker table w/ some cards shown as a way to test how well the code will detect the shown cards
test_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)


#loop for matching
for tmp in template_data:
    
#for tmp in template_names:
    #for img_name in template_names:
    (tH, tW) = tmp.shape[:2]
    #cv2.imshow("Template", tmpl)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    result = cv2.matchTemplate(test_image, tmp, cv2.TM_CCOEFF_NORMED)
    #threshold = 2
    ### new
    
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    ### end new
    #threshold = 0.8
    #loc = np.where(result >= threshold)
    ###min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    bottom_right = (top_left[0] + tW, top_left[1] + tH)
    #cv2.rectangle(test_image,top_left, bottom_right, 255, 2)
    threshold = 0.94 # the bigger the number the less precise, 94 seems to be alright, sort of
    #flag = False
   
    if np.amax(result) > threshold:
        flag = True
        otherres = cv2.rectangle(test_image,top_left, bottom_right, 75, 2)
        #print(otherres[0])
        #print(tmp[0])
        ## THE FOLLOWING LOOP IS THE REASON FOR SUPRESSED WARNING EARLIER, BUT THIS IS THE ONLY WAY I FIGURED TO EXTRACT NAMES OF MATCHED TEMPLATES
        for stuff in files1:
            #print(stuff)
            stuffs = cv2.imread(stuff,0)
            names = MyImage(stuff)
            comparison = stuffs[0] == tmp[0]
            
            #print((np.where(comparison)[0]),names)
            
            x = (str(names)+str(comparison))
            #print(x)
            spl_char = "True"
            ###res = x.split(spl_char, 1)[0]
            
            #print('\n'.join(cat(x) | grep(spl_char)))
            ###print(str(res))
            ### THE FOLLOWING IS EXTRACTING THE NAMES AND PRINTING THEM IN THE CONSOLE OUTPUT
            if re.search(spl_char, x):
                spl_char2 = "g\[ "
                if re.search(spl_char2, x):
                    #print(x)
                    spl_char3 = "png"
                    res = x.split(spl_char3, 1)[0]
                    m = re.search(r"\[([A-Za-z0-9_]+)\]", res)
                    print(m.group(1), end=",")
               
            #print(found)
            
            #char1 = '['
            #char2 = ' '
            #match = re.search(r'c.*g ', str(res))
            #print(match)
            #print(res[res.find(char1)+1 : res.find(char2)])
            
            # printing those lines 
                #print(res)
            #print re.findall(r'\[', x)
            #print(names)
            #print(names)
            #if stuffs[0].all() == tmp[0].all():
            #    print(stuffs[0], tmp[0], flag, names)
            #np.where(stuffs.all() > tmp.all(), print(names), print(flag))
                #print("Array stuff: ", stuffs)
                #print("Array tmp: ", tmp)
                #print("stuffs eq template")
                #print(np.greater(stuffs, tmp))
        #        print(l,x)
        #print(flag)
        #flag = True
        #val = (flag, flag)
        #for img_name in template_names:
        #print(tmp, image_name)
    
            
cv2.imshow('Result',test_image) # not needed for what I wanted to make with this, it's more for debugging, determining how properly found matches have been detected
cv2.waitKey(0)
